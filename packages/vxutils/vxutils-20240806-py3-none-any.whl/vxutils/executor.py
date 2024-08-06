"""Implements a thread pool executor."""

__author__ = "vex1023 (libao@vxquant.com)"

import logging
from concurrent.futures import Future, BrokenExecutor, Executor
import itertools
import queue
import threading
import os
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    Set,
    Sequence,
    Tuple,
)
from vxutils import VXContext


class BrokenThreadPool(BrokenExecutor):
    pass


class VXTaskItem:
    def __init__(
        self,
        func: Callable[..., Any],
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
    ) -> None:
        self.future: Future[Any] = Future()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, context: VXContext) -> None:
        if not self.future.set_running_or_notify_cancel():
            return

        try:
            result = self.func(*self.args, **self.kwargs)
            self.future.set_result(result)
        except BaseException as exc:
            self.future.set_exception(exc)


class VXBasicWorkerFactory(threading.Thread):
    """工作线程基类

    Arguments:
        work_queue {queue.Queue[VXTaskItem]} -- 任务队列
        idle_semaphore {threading.Semaphore} -- 信号量
        context {Optional[VXContext]} -- 上下文
        name {str} -- 线程名称
        idle_timeout {int} -- 空闲超时时间
    """

    def __init__(
        self,
        work_queue: queue.Queue[Optional[VXTaskItem]],
        idle_semaphore: threading.Semaphore,
        context: Optional[VXContext] = None,
        name: str = "",
        idle_timeout: Optional[int] = None,
    ) -> None:
        self._idle_semaphore = idle_semaphore
        self._idle_timeout = idle_timeout
        self._work_queue = work_queue
        self._context = context if context is not None else VXContext()
        return super().__init__(name=name, daemon=True, target=self.__worker_run__)

    @property
    def context(self) -> VXContext:
        """上下文"""
        return self._context

    def pre_run(self) -> None:
        logging.debug("worker %s start", self.name)

    def post_run(self) -> None:
        logging.debug("worker %s stop", self.name)

    def __worker_run__(self) -> None:
        try:
            self.pre_run()
        except BaseException as err:
            logging.error("worker pre_run error: %s", err, exc_info=True)
            raise BrokenThreadPool(err)

        try:
            while True:
                try:
                    task = self._work_queue.get_nowait()
                except queue.Empty:
                    self._idle_semaphore.release()
                    task = self._work_queue.get(timeout=self._idle_timeout)

                if task is None:
                    break

                task(self.context)
        except queue.Empty:
            pass

        finally:
            self._idle_semaphore.acquire(timeout=0)
            self.post_run()


class VXBasicPool:

    _counter = itertools.count().__next__

    def __init__(
        self,
        max_workers: Optional[int] = None,
        thread_name_prefix: str = "",
        worker_factory: Type[VXBasicWorkerFactory] = VXBasicWorkerFactory,
        context: Optional[VXContext] = None,
        idle_timeout: int = 600,
    ) -> None:
        """Initializes a new VXExecutor instance.

        Args:
            max_workers: The maximum number of threads that can be used to
                execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
            worker_factory: The factory class to create worker threads.
            context: The context to pass to worker threads.
            idle_timeout: The timeout in seconds to wait for a new task.

        """
        if max_workers is None:
            # VXExecutor is often used to:
            # * CPU bound task which releases GIL
            # * I/O bound task (which releases GIL, of course)
            #
            # We use cpu_count + 4 for both types of tasks.
            # But we limit it to 32 to avoid consuming surprisingly large resource
            # on many core machine.
            max_workers = min(32, (os.cpu_count() or 1) + 4)
        if max_workers <= 0:
            raise ValueError("max_workers must be greater than 0")

        self._max_workers = max_workers
        self._work_queue: queue.Queue[Optional[VXTaskItem]] = queue.Queue()
        self._idle_semaphore = threading.Semaphore(0)
        self._threads: Set[threading.Thread] = set()
        self._broken = False
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._thread_name_prefix = thread_name_prefix or self.__class__.__name__
        self._context = context if context is not None else VXContext()
        self._worker_factory = worker_factory
        self._idle_timeout = idle_timeout

    def submit(self, task: VXTaskItem) -> Future[Any]:
        """提交任务

        Arguments:
            task {VXTaskItem} -- 提交的任务

        Returns:
            Future[Any] -- 返回任务的 Future
        """

        with self._shutdown_lock:
            if self._broken:
                raise BrokenThreadPool(self._broken)

            if self._shutdown:
                raise RuntimeError("cannot schedule new futures after shutdown")

            self._work_queue.put(task)
            self._adjust_thread_count()
            return task.future

    def map(self, tasks: Sequence[VXTaskItem]) -> List[Any]:
        """批量提交任务

        Arguments:
            tasks {List[VXTaskItem]} -- 待提交的任务

        Raises:
            BrokenThreadPool: _description_
            RuntimeError: _description_

        Returns:
            Sequence[Future[Any]] -- 返回任务的 Future 列表
        """

        with self._shutdown_lock:
            if self._broken:
                raise BrokenThreadPool(self._broken)

            if self._shutdown:
                raise RuntimeError("cannot schedule new futures after shutdown")

            for task in tasks:
                self._work_queue.put(task)
                self._adjust_thread_count()
        return [task.future.result() for task in tasks]

    def _adjust_thread_count(self) -> None:
        # if idle threads are available, don't spin new threads
        if self._idle_semaphore.acquire(timeout=0):
            return

        self._threads = {t for t in self._threads if t.is_alive()}
        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = "%s_%d" % (
                self._thread_name_prefix or self,
                self._counter(),
            )
            t = self._worker_factory(
                self._work_queue,
                self._idle_semaphore,
                self._context,
                name=thread_name,
                idle_timeout=self._idle_timeout,
            )
            t.start()
            self._threads.add(t)

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False) -> None:
        with self._shutdown_lock:
            self._shutdown = True
            if cancel_futures:
                # Drain all work items from the queue, and then cancel their
                # associated futures.
                while not self._work_queue.empty():
                    try:
                        work_item = self._work_queue.get_nowait()
                    except queue.Empty:
                        break
                    if work_item is not None:
                        work_item.future.cancel()

            # Send a wake-up to prevent threads calling
            # _work_queue.get(block=True) from permanently blocking.
            for t in self._threads:
                self._work_queue.put(None)
        if wait:
            for t in self._threads:
                t.join()


class VXExecutor(Executor):
    """A thread pool executor.

    This class is a simple wrapper around the Python standard library's
    ThreadPoolExecutor class. It provides a more convenient way to create
    and manage thread pools.

    """

    def __init__(
        self,
        max_workers: Optional[int] = None,
        thread_name_prefix: str = "",
    ) -> None:
        """Initializes a new VXExecutor instance."""
        self._executor = VXBasicPool(max_workers, thread_name_prefix, idle_timeout=None)
        super().__init__()

    def submit(
        self, fn: Callable[..., Any], /, *args: Any, **kwargs: Any
    ) -> Future[Any]:
        """Submits a callable to be executed with the given arguments.

        Args:
            fn: The callable to execute.
            *args: The arguments to pass to the callable.
            **kwargs: The keyword arguments to pass to the callable.

        Returns:
            A Future representing the result of the callable.

        """
        task = VXTaskItem(fn, args, kwargs)
        return self._executor.submit(task)

    def shutdown(self, wait: bool = True, *, cancel_futures: bool = False) -> None:
        self._executor.shutdown(wait, cancel_futures=cancel_futures)
        return super().shutdown(wait, cancel_futures=cancel_futures)
