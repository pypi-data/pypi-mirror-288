#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ilya Egorov <0x42005e1f@gmail.com>
# SPDX-License-Identifier: ISC

__all__ = (
    'shield',
    'checkpoint',
    'checkpoint_if_cancelled', 'cancel_shielded_checkpoint',
)

try:
    from anyio import CancelScope
    from anyio.lowlevel import (
        checkpoint,
        checkpoint_if_cancelled,
        cancel_shielded_checkpoint,
    )
except ImportError:
    from .libraries import (
        AsyncLibraryNotFoundError,
        trio_running,
        current_async_library,
    )
    
    try:
        from asyncio import (
            sleep as asyncio_sleep,
            shield as asyncio_shield,
        )
    except ImportError:
        async def asyncio_shield(coro):
            raise NotImplementedError
        
        async def asyncio_checkpoint():
            pass
        
        async def asyncio_cancel_shielded_checkpoint():
            pass
    else:
        async def asyncio_checkpoint():
            await asyncio_sleep(0)
        
        async def asyncio_cancel_shielded_checkpoint():
            await asyncio_shield(asyncio_sleep(0))
    
    try:
        from trio import CancelScope
        from trio.lowlevel import (
            checkpoint as trio_checkpoint,
            checkpoint_if_cancelled as trio_checkpoint_if_cancelled,
            cancel_shielded_checkpoint as trio_cancel_shielded_checkpoint,
        )
    except ImportError:
        async def trio_shield(coro):
            raise NotImplementedError
        
        async def trio_checkpoint():
            pass
        
        async def trio_checkpoint_if_cancelled():
            pass
        
        async def trio_cancel_shielded_checkpoint():
            pass
    else:
        async def trio_shield(coro):
            with CancelScope(shield=True):
                return await coro
    
    async def shield(coro):
        library = current_async_library()
        
        if library == 'asyncio':
            result = await asyncio_shield(coro)
        elif library == 'trio':
            result = await trio_shield(coro)
        else:
            raise RuntimeError(f"unsupported async library {library!r}")
        
        return result
    
    async def checkpoint():
        try:
            library = current_async_library()
        except AsyncLibraryNotFoundError:
            pass
        else:
            if library == 'asyncio':
                await asyncio_checkpoint()
            elif library == 'trio':
                await trio_checkpoint()
    
    async def checkpoint_if_cancelled():
        if trio_running():
            await trio_checkpoint_if_cancelled()
    
    async def cancel_shielded_checkpoint():
        try:
            library = current_async_library()
        except AsyncLibraryNotFoundError:
            pass
        else:
            if library == 'asyncio':
                await asyncio_cancel_shielded_checkpoint()
            elif library == 'trio':
                await trio_cancel_shielded_checkpoint()
else:
    async def shield(coro):
        with CancelScope(shield=True):
            return await coro
