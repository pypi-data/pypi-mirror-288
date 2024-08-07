#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ilya Egorov <0x42005e1f@gmail.com>
# SPDX-License-Identifier: ISC

__all__ = (
    'AsyncLibraryNotFoundError',
    'asyncio_running', 'trio_running',
    'current_async_library',
)

try:
    from sniffio import AsyncLibraryNotFoundError, current_async_library
except ImportError:
    class AsyncLibraryNotFoundError(RuntimeError):
        pass
    
    try:
        from asyncio import current_task as current_asyncio_task
    except ImportError:
        def asyncio_running():
            return False
    else:
        def asyncio_running():
            try:
                running = current_asyncio_task() is not None
            except RuntimeError:
                running = False
            
            return running
    
    try:
        from trio.lowlevel import current_task as current_trio_task
    except ImportError:
        def trio_running():
            return False
    else:
        def trio_running():
            try:
                running = current_trio_task() is not None
            except RuntimeError:
                running = False
            
            return running
    
    def current_async_library():
        if asyncio_running():
            library = 'asyncio'
        elif trio_running():
            library = 'trio'
        else:
            raise AsyncLibraryNotFoundError(
                'unknown async library, or not in async context',
            )
        
        return library
else:
    def asyncio_running():
        try:
            running = current_async_library() == 'asyncio'
        except AsyncLibraryNotFoundError:
            running = False
        
        return running
    
    def trio_running():
        try:
            running = current_async_library() == 'trio'
        except AsyncLibraryNotFoundError:
            running = False
        
        return running
