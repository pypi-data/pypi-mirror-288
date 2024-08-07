#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ilya Egorov <0x42005e1f@gmail.com>
# SPDX-License-Identifier: ISC

__all__ = (
    'DUMMY_EVENT',
    'ThreadEvent',
    'TaskEvent', 'AsyncioEvent', 'TrioEvent',
)

from abc import ABC, abstractmethod

from .libraries import current_async_library
from .checkpoints import checkpoint


class DummyEvent:
    __slots__ = ()
    
    @staticmethod
    def __new__(cls, /):
        if cls is DummyEvent:
            self = DUMMY_EVENT
        else:
            self = super(DummyEvent, cls).__new__(cls)
        
        return self
    
    @classmethod
    def __init_subclass__(cls, /, **kwargs):
        raise TypeError("type 'DummyEvent' is not an acceptable base type")
    
    def __reduce__(self, /):
        return 'DUMMY_EVENT'
    
    def __repr__(self, /):
        return 'DUMMY_EVENT'
    
    def __bool__(self, /):
        return True
    
    def __await__(self, /):
        yield from checkpoint().__await__()
        
        return True
    
    def wait(self, /, timeout=None):
        return True
    
    def set(self, /):
        pass
    
    def is_set(self, /):
        return True


DUMMY_EVENT = object.__new__(DummyEvent)

try:
    from _thread import allocate_lock
except ImportError:
    try:
        from threading import Event as ThreadEvent
    except ImportError:
        import time
        
        class ThreadEvent:
            __slots__ = (
                '__is_unset',
            )
            
            @staticmethod
            def __new__(cls, /):
                self = super(ThreadEvent, cls).__new__(cls)
                
                self.__is_unset = True
                
                return self
            
            @classmethod
            def __init_subclass__(cls, /, **kwargs):
                raise TypeError(
                    "type 'ThreadEvent' is not an acceptable base type",
                )
            
            def __reduce__(self, /):
                raise TypeError(f"cannot reduce {self!r}")
            
            def wait(self, /, timeout=None):
                if timeout is not None:
                    deadline = time.monotonic() + timeout
                
                success = False
                
                while self.__is_unset:
                    if timeout is not None:
                        if time.monotonic() >= deadline:
                            break
                    
                    time.sleep(0)
                else:
                    success = True
                
                return success
            
            def set(self, /):
                self.__is_unset = False
            
            def is_set(self, /):
                return not self.__is_unset
else:
    class ThreadEvent:
        __slots__ = (
            '__is_unset',
            'lock',
        )
        
        @staticmethod
        def __new__(cls, /):
            self = super(ThreadEvent, cls).__new__(cls)
            
            self.__is_unset = [True]
            
            self.lock = allocate_lock()
            self.lock.acquire()
            
            return self
        
        @classmethod
        def __init_subclass__(cls, /, **kwargs):
            raise TypeError(
                "type 'ThreadEvent' is not an acceptable base type",
            )
        
        def __reduce__(self, /):
            raise TypeError(f"cannot reduce {self!r}")
        
        def wait(self, /, timeout=None):
            if self.__is_unset:
                if timeout is None:
                    success = self.lock.acquire()
                else:
                    success = self.lock.acquire(timeout=timeout)
            else:
                success = True
            
            return success
        
        def set(self, /):
            if self.__is_unset:
                try:
                    self.__is_unset.pop()
                except IndexError:
                    pass
                else:
                    self.lock.release()
        
        def is_set(self, /):
            return not self.__is_unset


class TaskEvent(ABC):
    __slots__ = ()
    
    @staticmethod
    def __new__(cls, /):
        if cls is TaskEvent:
            library = current_async_library()
            
            if library == 'asyncio':
                self = AsyncioEvent.__new__(AsyncioEvent)
            elif library == 'trio':
                self = TrioEvent.__new__(TrioEvent)
            else:
                raise RuntimeError(f"unsupported async library {library!r}")
        else:
            self = super(TaskEvent, cls).__new__(cls)
        
        return self
    
    @abstractmethod
    def __bool__(self, /):
        return self.is_set()
    
    @abstractmethod
    def __await__(self, /):
        raise NotImplementedError
    
    @abstractmethod
    def set(self, /):
        raise NotImplementedError
    
    @abstractmethod
    def is_set(self, /):
        return bool(self)


try:
    from asyncio import get_running_loop as get_running_asyncio_loop
except ImportError:
    class AsyncioEvent(TaskEvent):
        __slots__ = ()
else:
    class AsyncioEvent(TaskEvent):
        __slots__ = (
            '__is_unset',
            'loop', 'future',
        )
        
        @staticmethod
        def __new__(cls, /):
            self = super(AsyncioEvent, cls).__new__(cls)
            
            self.__is_unset = [True]
            
            self.loop = get_running_asyncio_loop()
            self.future = None
            
            return self
        
        @classmethod
        def __init_subclass__(cls, /, **kwargs):
            raise TypeError(
                "type 'AsyncioEvent' is not an acceptable base type",
            )
        
        def __reduce__(self, /):
            raise TypeError(f"cannot reduce {self!r}")
        
        def __bool__(self, /):
            return not self.__is_unset
        
        def __await__(self, /):
            if self.__is_unset:
                self.future = self.loop.create_future()
                
                try:
                    yield from self.future.__await__()
                except BaseException:
                    self.future = None
                    
                    try:
                        self.__is_unset.pop()
                    except IndexError:
                        pass
                    
                    raise
            else:
                yield from checkpoint().__await__()
            
            return True
        
        def set(self, /):
            if self.__is_unset:
                try:
                    self.__is_unset.pop()
                except IndexError:
                    pass
                else:
                    try:
                        loop = get_running_asyncio_loop()
                    except RuntimeError:  # no running event loop
                        loop = None
                    
                    if loop is self.loop:
                        if self.future is not None:
                            self.future.set_result(True)
                    else:
                        try:
                            self.loop.call_soon_threadsafe(lambda: (
                                self.future.set_result(True)
                                if self.future is not None else
                                None
                            ))
                        except RuntimeError:  # event loop is closed
                            pass
        
        def is_set(self, /):
            return not self.__is_unset


try:
    from trio import RunFinishedError
    from trio.lowlevel import (
        Abort,
        reschedule as reschedule_trio_task,
        current_task as current_trio_task,
        current_trio_token,
        wait_task_rescheduled as wait_trio_task_rescheduled,
    )
except ImportError:
    class TrioEvent(TaskEvent):
        __slots__ = ()
else:
    class TrioEvent(TaskEvent):
        __slots__ = (
            '__is_unset',
            'token', 'task',
        )
        
        @staticmethod
        def __new__(cls, /):
            self = super(TrioEvent, cls).__new__(cls)
            
            self.__is_unset = [True]
            
            self.token = current_trio_token()
            self.task = None
            
            return self
        
        @classmethod
        def __init_subclass__(cls, /, **kwargs):
            raise TypeError("type 'TrioEvent' is not an acceptable base type")
        
        def __reduce__(self, /):
            raise TypeError(f"cannot reduce {self!r}")
        
        def __bool__(self, /):
            return not self.__is_unset
        
        def __await__(self, /):
            if self.__is_unset:
                self.task = current_trio_task()
                
                def abort(_):
                    self.task = None
                    
                    try:
                        self.__is_unset.pop()
                    except IndexError:
                        pass
                    
                    return Abort.SUCCEEDED
                
                yield from wait_trio_task_rescheduled(abort).__await__()
            else:
                yield from checkpoint().__await__()
            
            return True
        
        def set(self, /):
            if self.__is_unset:
                try:
                    self.__is_unset.pop()
                except IndexError:
                    pass
                else:
                    try:
                        token = current_trio_token()
                    except RuntimeError:  # no called trio.run
                        token = None
                    
                    if token is self.token:
                        if self.task is not None:
                            reschedule_trio_task(self.task)
                    else:
                        try:
                            self.token.run_sync_soon(lambda: (
                                reschedule_trio_task(self.task)
                                if self.task is not None else
                                None
                            ))
                        except RunFinishedError:
                            pass
        
        def is_set(self, /):
            return not self.__is_unset
