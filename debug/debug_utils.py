from .vlog import log
from .debug_flags import DBG_OPS

import functools

def log_exec(func):
    @functools.wraps(func)
    def wrapper(self, context, *args, **kwargs):
        if DBG_OPS:
            log.header(f"Starting {self.bl_idname} Execution")
            log.increase()
        result = func(self, context, *args, **kwargs)
        if DBG_OPS:
            log.decrease()
            log.info(f"Finished {self.bl_idname}")
        return result
    return wrapper
