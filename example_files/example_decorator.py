"""
Examples: @trace decorator - sync functions, async functions, stacked decorators

Run this file directly to execute all examples (uncomment calls in __main__).
"""

# ============================================================
# Imports
# ============================================================

import asyncio
import functools
from taipan_logger import taipan, configure, trace

configure(debug=True)

# ============================================================
# Example: Basic sync function tracing
# ============================================================

@trace
def add(x: int, y: int) -> int:
    # @trace logs entry args, return type, and elapsed time automatically
    return x + y


@trace
def greet(name: str) -> str:
    taipan.info("Greeting someone")
    return f"Hello {name}"


@trace
def no_args_no_return() -> None:
    # Works with functions that take and return nothing
    taipan.debug("Doing something quietly")


def example_sync_trace() -> None:
    add(3, 7)
    greet("Sora")
    no_args_no_return()


# ============================================================
# Example: Async function tracing
# ============================================================

@trace
async def async_fetch(url: str) -> dict:
    # @trace detects coroutines automatically - no extra config needed
    await asyncio.sleep(0.05)
    return {"url": url, "status": 200}


@trace
async def async_no_return() -> None:
    await asyncio.sleep(0.02)
    taipan.warning("Async warning from inside")


async def example_async_trace() -> None:
    await async_fetch("https://example.com")
    await async_no_return()


# ============================================================
# Example: Stacked decorators
# ============================================================

def repeat(times: int):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


# @trace must be closest to the function - the outer decorator calls the traced version
@repeat(times=3)
@trace
def say_hello(name: str) -> str:
    return f"Hello {name}"


@repeat(times=2)
@trace
def multiply(x: int, y: int) -> int:
    return x * y


def example_stacked_decorators() -> None:
    say_hello("Sam")
    multiply(3, 7)


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    # Uncomment to run individual examples
    # example_sync_trace()
    # asyncio.run(example_async_trace())
    # example_stacked_decorators()
    pass
