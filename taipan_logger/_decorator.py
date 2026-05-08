"""
Provides the @trace decorator for automatic call logging on sync and async functions.
Logs entry parameters, return type, elapsed time, and any exceptions via the taipan logger.
Works on regular functions, methods, and dunder methods.

:author: sora7672
"""

__author__: str = "sora7672"

import asyncio
import functools

from uuid import uuid4
from time import monotonic
from ._logger import TaipanLogger


def _get_formatted_var_info(var: any) -> str:
    """
    Builds a compact type-info string for a single variable.
    For collections, lists the element types inline.
    For dicts, lists key-value type pairs inline.

    :param var: any (The variable to describe)
    :return: str (Formatted type info string)
    """
    if var is None:
        return "None"
    elif callable(var):
        return "callable"

    var_type = type(var).__name__
    out = var_type
    match var_type:
        case "int":
            out += f"(digits: {len(str(var))})"
        case "float":
            decimal_part = str(var).split(".")
            out += f"(digits after comma: {len(decimal_part[1]) if len(decimal_part) > 1 else 0})"
        case "str":
            out += f"(length: {len(var)})"
        case "list" | "tuple" | "set" | "frozenset":
            out += "[ "
            for i in var:
                out += f"{type(i).__name__}, "
            out += "]"
        case "dict":
            out += "{ "
            for key, value in var.items():
                out += f"{key}: {type(value).__name__}, "
            out += "}"
        case _:
            pass

    return out


def _get_xargs_kwargs_info(*xargs, **kwargs) -> str:
    """
    Builds a formatted string summarizing the types and structure of all
    positional and keyword arguments passed to a traced function.
    Each positional arg is indexed, each keyword arg is shown by name.

    :param xargs: any (Positional arguments to describe)
    :param kwargs: any (Keyword arguments to describe)
    :return: str (Formatted summary string, empty if no arguments were passed)
    """
    if not xargs and not kwargs:
        return "0 xargs and 0 kwargs"

    out = "\n"

    if xargs:
        out += f"    {len(xargs)} xargs: "
        out += ", ".join(f"[{i}] {_get_formatted_var_info(arg)}" for i, arg in enumerate(xargs))

    if xargs and kwargs:
        out += "\n"
    if kwargs:
        out += f"    {len(kwargs)} kwargs: "
        out += ", ".join(f"[{key}] {_get_formatted_var_info(value)}" for key, value in kwargs.items())

    return out

def trace(func):
    """
    Decorator that wraps a sync or async function with automatic trace logging.
    Generates a unique trace_id per call and logs entry, exit, and exceptions.
    Exceptions are always re-raised after logging.

    :param func: the function to wrap
    :return: async_wrapper if the function is a coroutine, sync_wrapper otherwise
    """

    @functools.wraps(func)
    async def async_wrapper(*xargs, **kwargs):
        """
        Async variant of the trace wrapper.
        Logs before and after the awaited call, or logs and re-raises on exception.

        :param xargs: positional arguments passed to the wrapped function
        :param kwargs: keyword arguments passed to the wrapped function
        :return: the return value of the wrapped function
        """
        trace_id: str = uuid4().hex[:8]
        start_time: float = monotonic()
        TaipanLogger.debug(
            message=f"|async||BeforeFunction| Argument infos: {_get_xargs_kwargs_info(*xargs,**kwargs)}",
            trace_id=trace_id, func_name=func.__name__
        )
        try:
            out = await func(*xargs, **kwargs)
        except Exception as e:
            if not TaipanLogger._exception_id_exists(id(e)):
                if TaipanLogger.has_exception_hook_in():
                    TaipanLogger.error(
                        message=f"{type(e).__name__}: An exception hook in is configured and should be shown below:",
                        trace_id=trace_id, func_name=func.__name__)
                else:
                    TaipanLogger.error(message=f"{type(e).__name__}: {e}", trace_id=trace_id, func_name=func.__name__)

            raise
        elapsed: float = monotonic() - start_time
        TaipanLogger.debug(message=f"|async||AfterFunction| Time needed {elapsed:.3f}s returns {_get_formatted_var_info(out)}",
                     trace_id=trace_id, func_name=func.__name__)
        return out

    @functools.wraps(func)
    def sync_wrapper(*xargs, **kwargs):
        """
        Sync variant of the trace wrapper.
        Logs before and after the call, or logs and re-raises on exception.

        :param xargs: positional arguments passed to the wrapped function
        :param kwargs: keyword arguments passed to the wrapped function
        :return: the return value of the wrapped function
        """
        trace_id: str = uuid4().hex[:8]
        start_time: float = monotonic()
        TaipanLogger.debug(
            message=f"|BeforeFunction| Argument infos: {_get_xargs_kwargs_info(*xargs,**kwargs)}",
            trace_id=trace_id, func_name=func.__name__)
        try:
            out = func(*xargs, **kwargs)
        except Exception as e:
            if not TaipanLogger._exception_id_exists(id(e)):
                if TaipanLogger.has_exception_hook_in():
                    TaipanLogger.error(
                        message=f"{type(e).__name__}: An exception hook in is configured and should be shown below:",
                        trace_id=trace_id, func_name=func.__name__)
                else:
                    TaipanLogger.error(message=f"{type(e).__name__}: {e}", trace_id=trace_id, func_name=func.__name__)
            raise
        elapsed: float = monotonic() - start_time
        TaipanLogger.debug(message=f"|AfterFunction| Time needed {elapsed:.3f}s returns {_get_formatted_var_info(out)}",
                     trace_id=trace_id, func_name=func.__name__)
        return out

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


if __name__ == "__main__":
    print("Dont start the package files alone! The imports wont work like this!")