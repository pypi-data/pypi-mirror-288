#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2024 Ilya Egorov <0x42005e1f@gmail.com>
# SPDX-License-Identifier: ISC

__all__ = (
    'Flag',
)

from .markers import MISSING


class Flag:
    __slots__ = (
        'markers',
    )
    
    @staticmethod
    def __new__(cls, /, marker=MISSING):
        self = super(Flag, cls).__new__(cls)
        
        if marker is not MISSING:
            self.markers = [marker]
        else:
            self.markers = []
        
        return self
    
    def __getnewargs__(self, /):
        if markers := self.markers:
            try:
                args = (markers[0],)
            except IndexError:
                args = ()
        else:
            args = ()
        
        return args
    
    def __repr__(self, /):
        if markers := self.markers:
            try:
                marker_repr = repr(markers[0])
            except IndexError:
                marker_repr = ''
        else:
            marker_repr = ''
        
        return f"Flag({marker_repr})"
    
    def __bool__(self, /):
        return bool(self.markers)
    
    def get(self, /, default=MISSING, *, default_factory=MISSING):
        try:
            marker = self.markers[0]
        except IndexError:
            if default is not MISSING:
                marker = default
            elif default_factory is not MISSING:
                marker = default_factory()
            else:
                raise LookupError(self) from None
        
        return marker
    
    def set(self, /, marker=MISSING):
        markers = self.markers
        
        if not markers:
            if marker is MISSING:
                marker = object()
            
            markers.append(marker)
            
            if len(markers) > 1:
                del markers[1:]
        
        if marker is not MISSING:
            try:
                actual_marker = markers[0]
            except IndexError:
                success = False
            else:
                success = marker is actual_marker
        else:
            success = False
        
        return success
    
    def clear(self, /):
        self.markers.clear()
