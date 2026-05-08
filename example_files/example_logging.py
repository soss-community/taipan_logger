"""
Examples: basic taipan logging - all four log levels, with and without configure()

Run this file directly to execute all examples (uncomment calls in __main__).
"""

# ============================================================
# Imports
# ============================================================

from taipan_logger import taipan, configure

# ============================================================
# Example: Logging without configure (all defaults)
# ============================================================

def example_logging_defaults() -> None:
    # No configure() call - taipan auto-detects project root and writes to <root>/logs/
    taipan.info("Service started")
    taipan.warning("Something looks off")
    taipan.error("Something broke")
    # debug is off by default, this line will not appear in the log
    taipan.debug("This will not be written unless debug=True")


# ============================================================
# Example: Logging with configure (custom prefix, debug on)
# ============================================================

def example_logging_configured() -> None:
    # configure() must be called before the first log entry
    configure(special_prefix="MY-SERVICE", debug=True)

    taipan.info("Service started")
    taipan.warning("Config value looks unusual")
    taipan.error("Database connection failed")
    # debug is now enabled, this will appear
    taipan.debug("Query took 342ms")


# ============================================================
# Example: Manual trace_id and func_name override
# ============================================================

def example_logging_manual_trace() -> None:
    # Useful when you want to group log lines manually without @trace
    my_trace = "abc12345"
    taipan.info("Starting batch job", trace_id=my_trace, func_name="batch_runner")
    taipan.info("Batch step 1 done", trace_id=my_trace, func_name="batch_runner")
    taipan.error("Batch step 2 failed", trace_id=my_trace, func_name="batch_runner")


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    # Uncomment to run individual examples
    # example_logging_defaults()
    # example_logging_configured()
    # example_logging_manual_trace()
    pass
