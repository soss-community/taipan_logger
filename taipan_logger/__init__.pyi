"""
Type stub for the taipan_logger public interface.
Provides static type information for IDEs and type checkers.
"""

from pathlib import Path

__author__: str
__version__: str
__date__: str
__description__: str

__all__: list[str]


def configure(field_order: list[str] | None = None, datetime_format: str | None = None,
              log_path: Path | str | None = None, log_path_relative: bool = True, log_name: str | None = None,
              max_old_logs: int | None = None, delete_older_logs: bool | None = None,
              special_prefix: str | None = None, exception_hook_in_is_set: bool = None,
              debug: bool | None = None, keep_log_open: bool | None = None,
              env_check_interval: int | None = None) -> None: ...

def trace(func: callable) -> callable: ...

class _Taipan:
    @classmethod
    def debug(cls, message: str, trace_id: str | None = None, func_name: str | None = None) -> None: ...

    @classmethod
    def info(cls, message: str, trace_id: str | None = None, func_name: str | None = None) -> None: ...

    @classmethod
    def warning(cls, message: str, trace_id: str | None = None, func_name: str | None = None) -> None: ...

    @classmethod
    def error(cls, message: str, trace_id: str | None = None, func_name: str | None = None) -> None: ...

    @classmethod
    def configure(cls, field_order: list[str] | None = None, datetime_format: str | None = None,
                  log_path: Path | str | None = None, log_path_relative: bool = True, log_name: str | None = None,
                  max_old_logs: int | None = None, delete_older_logs: bool | None = None,
                  special_prefix: str | None = None, exception_hook_in_is_set: bool = None,
                  debug: bool | None = None, keep_log_open: bool | None = None,
                  env_check_interval: int | None = None) -> None: ...

    @classmethod
    def has_exception_hook_in(cls) -> bool: ...

taipan: _Taipan
