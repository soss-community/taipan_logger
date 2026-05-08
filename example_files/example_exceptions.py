"""
Examples: exception handling with @trace - re-raise deduplication, hook_in mode

Each example must be called individually since unhandled exceptions abort execution.
Run this file directly to execute all examples (uncomment calls in __main__).
"""

# ============================================================
# Imports
# ============================================================

from taipan_logger import taipan, configure, trace

configure(debug=True)

# ============================================================
# Example: Basic exception - logged once, re-raised
# ============================================================

@trace
def will_fail() -> None:
    # @trace logs the exception at the frame where it occurs, then re-raises
    raise ValueError("I was always going to fail")


def example_exception_basic() -> None:
    try:
        will_fail()
    except ValueError:
        pass


# ============================================================
# Example: Exception deduplication across nested @trace frames
# ============================================================

@trace
def inner_fail() -> None:
    raise RuntimeError("Failure in inner")


@trace
def outer_caller() -> None:
    # The same exception object bubbles up through outer_caller
    # @trace only logs it once - at inner_fail where it originated
    inner_fail()


def example_exception_deduplication() -> None:
    try:
        outer_caller()
    except RuntimeError:
        pass


# ============================================================
# Example: Wrapped exception - logged as a new distinct exception
# ============================================================

@trace
def source_error() -> None:
    raise ValueError("original problem")


@trace
def wrapping_caller() -> None:
    try:
        source_error()
    except ValueError as e:
        # raise ... from e creates a new exception object
        # @trace treats it as a separate exception and logs it too
        raise RuntimeError("Wrapped error") from e


def example_exception_wrapped() -> None:
    try:
        wrapping_caller()
    except RuntimeError:
        pass


# ============================================================
# Example: exception_hook_in_is_set - @trace defers exception output to external hook
# ============================================================

# When exception_hook_in_is_set=True, @trace skips logging the exception details.
# It only logs that a hook is configured and should handle the output.
# The hook (e.g. ladon-clear-exceptions-n-warnings) is responsible for formatting and writing.
#
# Minimal example without an actual hook - just shows the configure flag:
#
#   from taipan_logger import taipan, configure, trace
#   configure(debug=True, exception_hook_in_is_set=True)
#
#   @trace
#   def might_fail():
#       raise ValueError("something went wrong")
#
#   try:
#       might_fail()
#   except ValueError:
#       pass
#
# @trace will log: "ValueError: An exception hook in is configured and should be shown below:"
# The hook is then expected to log the actual exception content.


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    # Uncomment to run individual examples - one at a time, exceptions abort execution
    # example_exception_basic()
    # example_exception_deduplication()
    # example_exception_wrapped()
    pass
