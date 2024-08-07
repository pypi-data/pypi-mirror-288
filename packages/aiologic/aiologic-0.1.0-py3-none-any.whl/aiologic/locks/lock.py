#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ilya Egorov <0x42005e1f@gmail.com>
# SPDX-License-Identifier: ISC

__all__ = (
    'Lock', 'RLock',
)

from aiologic.lowlevel import current_task, current_thread

from .lot import ParkingLot


class Lock:
    __slots__ = (
        'lot',
        'owner_thread', 'owner_task',
    )
    
    @staticmethod
    def __new__(cls, /):
        self = super(Lock, cls).__new__(cls)
        
        self.lot = ParkingLot()
        self.lot.unpark(exact=True)
        
        self.owner_thread = None
        self.owner_task = None
        
        return self
    
    def __repr__(self, /):
        return 'Lock()'
    
    def __bool__(self, /):
        return not self.lot.pending
    
    async def __aenter__(self, /):
        await self.acquire_as_task()
        
        return self
    
    async def __aexit__(self, /, exc_type, exc_value, traceback):
        self.release_as_task()
    
    def __enter__(self, /):
        self.acquire_as_thread()
        
        return self
    
    def __exit__(self, /, exc_type, exc_value, traceback):
        self.release_as_thread()
    
    async def acquire_as_task(self, /):
        thread = current_thread()
        task = current_task()
        
        if self.owner_thread == thread:
            if self.owner_task is None:
                raise RuntimeError(
                    'the current thread is already holding this lock',
                )
            
            if self.owner_task == task:
                raise RuntimeError(
                    'the current task is already holding this lock',
                )
        
        success = await self.lot.park_as_task(exact=True)
        
        if success:
            self.owner_thread = thread
            self.owner_task = task
        
        return success
    
    def acquire_as_thread(self, /, *, blocking=True, timeout=None):
        thread = current_thread()
        
        if self.owner_thread == thread:
            raise RuntimeError(
                'the current thread is already holding this lock',
            )
        
        success = self.lot.park_as_thread(
            blocking=blocking,
            timeout=timeout,
            exact=True,
        )
        
        if success:
            self.owner_thread = thread
            self.owner_task = None
        
        return success
    
    def release_as_task(self, /):
        if self.owner_thread is None:
            raise RuntimeError('release unlocked lock')
        
        thread = current_thread()
        
        if self.owner_thread != thread:
            raise RuntimeError('the current thread is not holding this lock')
        
        task = current_task()
        
        if self.owner_task != task:
            raise RuntimeError('the current task is not holding this lock')
        
        self.owner_task = None
        self.owner_thread = None
        
        self.lot.unpark(exact=True)
    
    def release_as_thread(self, /):
        if self.owner_thread is None:
            raise RuntimeError('release unlocked lock')
        
        thread = current_thread()
        
        if self.owner_thread != thread:
            raise RuntimeError('the current thread is not holding this lock')
        
        if self.owner_task is not None:
            raise RuntimeError('the current task is not holding this lock')
        
        self.owner_thread = None
        
        self.lot.unpark(exact=True)
    
    def locked(self, /):
        return not self.lot.pending


class RLock:
    __slots__ = (
        'lot',
        'owner_thread', 'owner_task',
        'thread_level', 'task_level',
    )
    
    @staticmethod
    def __new__(cls, /):
        self = super(RLock, cls).__new__(cls)
        
        self.lot = ParkingLot()
        self.lot.unpark(exact=True)
        
        self.owner_thread = None
        self.owner_task = None
        
        self.thread_level = 0
        self.task_level = 0
        
        return self
    
    def __repr__(self, /):
        return 'RLock()'
    
    def __bool__(self, /):
        return not self.lot.pending
    
    async def __aenter__(self, /):
        await self.acquire_as_task()
        
        return self
    
    async def __aexit__(self, /, exc_type, exc_value, traceback):
        self.release_as_task()
    
    def __enter__(self, /):
        self.acquire_as_thread()
        
        return self
    
    def __exit__(self, /, exc_type, exc_value, traceback):
        self.release_as_thread()
    
    async def acquire_as_task(self, /):
        thread = current_thread()
        task = current_task()
        
        if self.owner_thread != thread or (
            self.owner_task is not None
            and self.owner_task != task
        ):
            success = await self.lot.park_as_task(exact=True)
            
            if success:
                self.owner_thread = thread
                self.owner_task = task
        else:
            self.owner_task = task
            
            success = True
        
        if success:
            self.task_level += 1
        
        return success
    
    def acquire_as_thread(self, /, *, blocking=True, timeout=None):
        thread = current_thread()
        
        if self.owner_thread != thread:
            success = self.lot.park_as_thread(
                blocking=blocking,
                timeout=timeout,
                exact=True,
            )
            
            if success:
                self.owner_thread = thread
                self.owner_task = None
        else:
            success = True
        
        if success:
            self.thread_level += 1
        
        return success
    
    async def _acquire_restore_as_task(self, /, state):
        thread, task, task_level = state
        
        success = await self.lot.park_as_task(exact=True)
        
        if success:
            self.owner_thread = thread
            self.owner_task = task
            
            self.task_level = task_level
        
        return success
    
    def _acquire_restore_as_thread(self, /, state):
        thread, task, thread_level, task_level = state
        
        success = self.lot.park_as_thread(exact=True)
        
        if success:
            self.owner_thread = thread
            self.owner_task = task
            
            self.thread_level = thread_level
            self.task_level = task_level
        
        return success
    
    def release_as_task(self, /):
        if self.owner_thread is None:
            raise RuntimeError('release unlocked lock')
        
        thread = current_thread()
        
        if self.owner_thread != thread:
            raise RuntimeError('the current thread is not holding this lock')
        
        task = current_task()
        
        if self.owner_task != task:
            raise RuntimeError('the current task is not holding this lock')
        
        self.task_level -= 1
        
        if not self.task_level:
            self.owner_task = None
        
        if not self.thread_level:
            self.owner_thread = None
            
            self.lot.unpark(exact=True)
    
    def release_as_thread(self, /):
        if self.owner_thread is None:
            raise RuntimeError('release unlocked lock')
        
        thread = current_thread()
        
        if self.owner_thread != thread:
            raise RuntimeError('the current thread is not holding this lock')
        
        if not self.thread_level:
            raise RuntimeError('the current task is not holding this lock')
        
        self.thread_level -= 1
        
        if not self.thread_level and self.owner_task is None:
            self.owner_thread = None
            
            self.lot.unpark(exact=True)
    
    def _release_save_as_task(self, /):
        if self.owner_thread is None:
            raise RuntimeError('release unlocked lock')
        
        thread = current_thread()
        
        if self.owner_thread != thread:
            raise RuntimeError('the current thread is not holding this lock')
        
        task = current_task()
        
        if self.owner_task != task:
            raise RuntimeError('the current task is not holding this lock')
        
        state = (thread, task, self.task_level)
        
        self.task_level = 0
        
        self.owner_task = None
        
        if not self.thread_level:
            self.owner_thread = None
            
            self.lot.unpark(exact=True)
        
        return state
    
    def _release_save_as_thread(self, /):
        if self.owner_thread is None:
            raise RuntimeError('release unlocked lock')
        
        thread = current_thread()
        
        if self.owner_thread != thread:
            raise RuntimeError('the current thread is not holding this lock')
        
        state = (thread, self.owner_task, self.thread_level, self.task_level)
        
        self.task_level = 0
        self.thread_level = 0
        
        self.owner_task = None
        self.owner_thread = None
        
        self.lot.unpark(exact=True)
        
        return state
    
    def locked(self, /):
        return not self.lot.pending
