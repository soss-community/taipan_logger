"""
Public interface of the taipan logger package.
Exposes the logger singleton, the configure function, and the trace decorator
for use by any code that imports this package.

:author: sora7672
"""

__author__: str = "sora7672"
__version__: str = "2.0.0"
__date__: str = "2026-05-09"
__description__: str = "A lightweight, GDPR-safe, threadsafe, async-ready Python logger."

from ._logger import TaipanLogger
from ._decorator import trace
from types import SimpleNamespace

taipan = SimpleNamespace()
taipan.__doc__ = taipan.__doc__ = """
Taipan logger instance. Provides structured log output with optional trace ID and function name.

Methods:
    .debug(message, trace_id=None, func_name=None)   - writes a DEBUG level log entry
    .info(message, trace_id=None, func_name=None)    - writes an INFO level log entry
    .warning(message, trace_id=None, func_name=None) - writes a WARNING level log entry
    .error(message, trace_id=None, func_name=None)   - writes an ERROR level log entry

:param message: str (the log message text)
:param trace_id: str | None (optional trace ID to group related log entries)
:param func_name: str | None (optional function name override, auto-detected if None)
"""
taipan.warning = TaipanLogger.warning
taipan.error = TaipanLogger.error
taipan.debug = TaipanLogger.debug
taipan.info = TaipanLogger.info
taipan.configure = TaipanLogger.configure
configure = TaipanLogger.configure


_public = {
    "taipan": taipan,
    "configure": configure,
    "trace": trace,
}

__all__ = list(_public.keys())

def __getattr__(name: str):
    if name not in __all__:
        print(f"'{name}' is not part of the public taipan API. Available: {__all__}")
    if name in _public:
        return _public[name]
    raise AttributeError(name)

if __name__ == "__main__":
    print("Dont start the package files alone! The imports wont work like this!")