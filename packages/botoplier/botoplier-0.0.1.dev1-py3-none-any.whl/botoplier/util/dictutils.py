import asyncio
from collections.abc import Awaitable
from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")


# From https://gist.github.com/privatwolke/11711cc26a843784afd1aeeb16308a30 (Public domain)
async def gather_dict(tasks: dict[K, Awaitable[V]]) -> dict[K, V]:
    """Return a dict of (key, returned_values) from a dict of (key, future)."""

    async def mark(key: K, coro: Awaitable[V]) -> tuple[K, V]:
        return key, await coro

    return dict(await asyncio.gather(*(mark(key, coro) for key, coro in tasks.items())))
