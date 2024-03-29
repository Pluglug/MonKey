import contextlib
import inspect
import time
import os


CONSOLE_COLOR_BLUE = '\033[34m'
CONSOLE_COLOR_RED = '\033[31m'
CONSOLE_COLOR_GREEN = '\033[1;32m'
CONSOLE_COLOR_YELLOW = '\033[33m'

CONSOLE_COLOR_LIGHT_BLUE = '\033[36m'
CONSOLE_COLOR_PURPLE = '\033[35m'
CONSOLE_COLOR_WHITE = '\033[37m'


class VisualLog:
    def __init__(self, package_id=""):
        self.package_id = package_id
        self.indent_level = 0
        self.inspect_enabled = False
        self.timer = None

    def enable_inspect(self):  # フラグ名と混同しやすい
        """Display the module name and line number of the caller."""
        self.inspect_enabled = True

    def disable_inspect(self):
        """Disable inspect."""
        self.inspect_enabled = False

    def _get_caller_info(self):
        if not self.inspect_enabled:
            return ""

        frame = inspect.currentframe()
        caller_frames = inspect.getouterframes(frame)
        current_script = os.path.basename(__file__)

        for outer_frame in caller_frames:
            module_name = outer_frame.filename
            if current_script not in module_name:
                line_number = outer_frame.lineno
                module_name = module_name if self.package_id in module_name else "Unknown module"
                module_name = os.path.relpath(module_name, os.path.dirname(__file__))
                return f"{module_name}:{line_number}: "
        return "Unknown module: "

    def _log(self, color, *args):
        caller_info = self._get_caller_info()
        indent = "  " * self.indent_level
        msg = caller_info + indent + ", ".join(str(arg) for arg in args)
        msg = msg.replace("\n", "\n" + indent)

        print(color + msg + '\033[0m')

    def header(self, msg, title=None):
        """Green text indicating the start of a new operation."""
        print("")

        if title is not None:
            title = str(title)
            header_length = max(len(msg), len(title)+8)
            title_text = title.center(header_length, '-')
            self._log(CONSOLE_COLOR_GREEN, title_text)

        self._log(CONSOLE_COLOR_GREEN, msg)
        return self

    def info(self, *args):
        """Blue text indicating the progress of an operation."""
        self._log(CONSOLE_COLOR_BLUE, *args)
        return self
    
    def error(self, *args):
        """Red text indicating an error that is not fatal."""
        self._log(CONSOLE_COLOR_RED, *args)
        return self

    def warn(self, *args):
        """Yellow text indicating a warning that is not fatal."""
        self._log(CONSOLE_COLOR_YELLOW, *args)
        self.error("warn() is deprecated. Use warning() instead.")
        return self

    def warning(self, *args):
        """Yellow text indicating a warning that is not fatal."""
        self.warn(*args)
        return self

    def __call__(self, *args):
        """Display the arguments in blue."""
        self.info(*args)
        return self

    # インデントはあんまり使わないかも
    @contextlib.contextmanager
    def indented(self):
        self.increase()
        try:
            yield
        finally:
            self.decrease()

    def indent(self, count=1):
        """Increase the indent level."""
        self.indent_level = max(0, self.indent_level + count)
        return self

    def increase(self, count=1):
        """Increase the indent level."""
        self.indent_level = max(0, self.indent_level + count)
        return self

    def decrease(self, count=1):
        """Decrease the indent level."""
        self.indent_level = max(0, self.indent_level - count)
        return self

    def reset_indent(self):
        """Reset the indent level to zero."""
        self.indent_level = 0
        return self
    
    def start_timer(self, msg="Timer started.", title=None):
        """Timer start and call header()"""
        self.header(msg, title)
        self.timer = time.time()
        return self

    def time(self, *args):
        """Display the elapsed time since the timer was started."""
        if self.timer is None:
            self.warn("Timer is not started.")
            return self

        now = time.time()
        self.info(f'{now - self.timer:.4f} sec', *args)
        return self
    
    def stop_timer(self, msg="Timer stopped.", *args):
        """Stop the timer"""
        self.time(msg, *args)
        self.timer = None
        return self

    # @classmethod
    # def get_instance(cls):
    #     return cls()

# log = VisualLog()


# Usage:
# log.header(msg)
# log.info(*args)
# log.error(*args)
# log.warning(*args)

# Memo: Should consider indenting like this:
# DBG_TREE and logi(" " * len(path) + "/".join(path))

if __name__ == "__main__":
    pass
