#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ilya Egorov <0x42005e1f@gmail.com>
# SPDX-License-Identifier: ISC

__all__ = (
    'current_thread',
    'current_token',
    'current_task',
)

from .libraries import current_async_library

try:
    from threading import get_ident as current_thread
except ImportError:
    def current_thread():
        return None

try:
    from anyio import get_current_task as current_task
    from anyio.lowlevel import current_token
except ImportError:
    try:
        from asyncio import (
            current_task as current_asyncio_task,
            get_running_loop as current_asyncio_token,
        )
    except ImportError:
        def current_asyncio_token():
            raise NotImplementedError
        
        def current_asyncio_task():
            raise NotImplementedError
    
    try:
        from trio.lowlevel import (
            current_task as current_trio_task,
            current_trio_token,
        )
    except ImportError:
        def current_trio_token():
            raise NotImplementedError
        
        def current_trio_task():
            raise NotImplementedError
    
    def current_token():
        library = current_async_library()
        
        if library == 'asyncio':
            token = current_asyncio_token()
        elif library == 'trio':
            token = current_trio_token()
        else:
            raise RuntimeError(f"unsupported async library {library!r}")
        
        return token
    
    def current_task():
        library = current_async_library()
        
        if library == 'asyncio':
            task = current_asyncio_task()
        elif library == 'trio':
            task = current_trio_task()
        else:
            raise RuntimeError(f"unsupported async library {library!r}")
        
        return task
