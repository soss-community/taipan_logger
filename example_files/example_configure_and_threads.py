"""
Examples: threading with @trace, configure() options, runtime debug toggle

Run this file directly to execute all examples (uncomment calls in __main__).
"""

# ============================================================
# Imports
# ============================================================

import threading
from taipan_logger import taipan, configure, trace

# ============================================================
# Example: configure() options
# ============================================================

def example_configure_custom() -> None:
    # All parameters are optional - set only what you need
    configure(
        special_prefix="MY-SERVICE",
        debug=True,
        log_name="myservice.log",
        max_old_logs=5,
        datetime_format="dd.MM.yyyy hh:mm:ss",
        field_order=["DATETIME", "LOG_STATUS", "THREAD", "FUNC_NAME", "MESSAGE"],
    )
    taipan.info("Configured with custom options")


def example_configure_minimal() -> None:
    # Minimum needed: nothing. All defaults work out of the box.
    # configure() is optional unless you want to change something.
    taipan.info("Running with all defaults")


def example_configure_custom_datetime() -> None:
    # taipan placeholder format - mix and match tokens freely
    configure(datetime_format="dd~MM~yy §hh:mm'ss§ [mimimi]")
    # Output: [08~05~26 §19:51'51§ [381]]
    taipan.info("Custom datetime format active")


# ============================================================
# Example: Threading - @trace is thread-safe, THREAD field shows thread name
# ============================================================

@trace
def thread_worker(worker_id: int) -> int:
    taipan.info(f"Worker {worker_id} started")
    result = worker_id * 2
    taipan.debug(f"Worker {worker_id} finished")
    return result


def example_threads() -> None:
    configure(debug=True)
    threads = []

    for i in range(4):
        # Thread name appears in [THREAD] field of every log line from that thread
        t = threading.Thread(target=thread_worker, args=(i,), name=f"Worker-{i}")
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    taipan.info("All workers done")


# ============================================================
# Example: Runtime debug toggle via environment variable
# ============================================================

def example_runtime_debug_toggle() -> None:
    # Set DEBUG_ENABLED=true in the environment to enable debug at runtime
    # without restarting the process. Taipan polls this every env_check_interval seconds.
    #
    # Shell:
    #   export DEBUG_ENABLED=true
    #   export DEBUG_ENABLED=false
    #
    # Or in Python (for testing only):
    import os
    os.environ["DEBUG_ENABLED"] = "true"
    # Next poll cycle will pick this up (default: every 120s)
    taipan.info("Debug will activate on next env check cycle")


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    # Uncomment to run individual examples
    # example_configure_minimal()
    # example_configure_custom()
    # example_configure_custom_datetime()
    # example_threads()
    # example_runtime_debug_toggle()
    pass
