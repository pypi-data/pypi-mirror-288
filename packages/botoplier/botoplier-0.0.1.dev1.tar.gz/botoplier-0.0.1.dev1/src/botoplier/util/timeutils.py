from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, ParamSpec, TypeVar

    LoggerFn = Callable[[str], None]

    P = ParamSpec("P")
    T = TypeVar("T")


def time_usage(logger_fn: LoggerFn) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """A decorator that will log timing of the decorated function every time it's called."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        def timeusage_wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            beg_ts = time.time()
            retval = func(*args, **kwargs)
            end_ts = time.time()
            # XXX correct for stack depth similar to loguru's .opt(depth=1)
            logger_fn(f"{func.__name__}(...) took %.03fs" % (end_ts - beg_ts))
            return retval

        return timeusage_wrapper

    return decorator
