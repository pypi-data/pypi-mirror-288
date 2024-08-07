"""Commonly used types.

import ucan.typing as snt

snt.Callable[..., snt.Awaitable[str]]
"""

from collections.abc import Awaitable, Callable, Coroutine


__all__ = ("Awaitable", "Callable", "Coroutine")
