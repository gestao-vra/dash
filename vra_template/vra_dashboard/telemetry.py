from contextlib import contextmanager
import logging
from time import perf_counter
log = logging.getLogger("vra_dashboard.performance")
@contextmanager
def timed(operation: str, **context: object):
    started = perf_counter()
    try: yield
    finally: log.info("timing operation=%s milliseconds=%.1f context=%s", operation, (perf_counter()-started)*1000, context)
