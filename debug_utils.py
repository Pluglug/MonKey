from enum import Enum
import contextlib
import traceback
import inspect
import time
import os


# Create global debug flags for the project
# Must have "DBG" prefix
DBG = True
DBG_INIT = True
DBG_OPS = True
DBG_PREFS = True
DBG_OVLY = True


class Color(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    BRIGHT_BLACK = 90
    BRIGHT_RED = 91
    BRIGHT_GREEN = 92
    BRIGHT_YELLOW = 93
    BRIGHT_BLUE = 94
    BRIGHT_MAGENTA = 95
    BRIGHT_CYAN = 96
    BRIGHT_WHITE = 97
    # Add 10 if using background colors
    # ansi(Color.WHITE + 10)

class Style(Enum):
    RESET = 0
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    INVERTED = 7

def ansi(*styles):
    return '\033[{}m'.format(";".join(str(color.value) for color in styles))


class PrintLog:
    def __init__(self):
        self.indent_level = 0
        self.track_caller_location = False
        self.use_colors = True
        self.timer = None
        self.line_length = 50

    def _get_caller_location(self):
        if not self.track_caller_location:
            return ""

        frame = traceback.extract_stack(None, 4)[0]  # Get caller's frame
        module_name = frame.filename.split('\\')[-1]
        return f"{module_name.ljust(10)}: {str(frame.lineno).ljust(4)} {frame.name.ljust(10)}: "

    def _log(self, color, *args):
        caller_info = self._get_caller_location()
        indent = "  " * self.indent_level
        msg = caller_info + indent + ", ".join(str(arg) for arg in args)
        msg = msg.replace("\n", "\n" + indent)

        if self.use_colors:
            print(color + msg + ansi(Style.RESET))
        else:
            print(msg)

    def header(self, msg, title=None):
        """Green text indicating the start of a new operation."""
        print("")

        if title is not None:
            title = str(title)
            header_length = max(len(msg), self.line_length)  # len(title)+8)
            title_text = title.center(header_length, '-')
            self._log(ansi(Color.GREEN, Style.BOLD), title_text)

        if msg:
            self._log(ansi(Color.GREEN, Style.BOLD), msg)

        return self
    
    def footer(self, *args):
        """Green text indicating the end of an operation."""
        self.reset_indent()
        self._log(ansi(Color.CYAN), *args)
        self._log(ansi(Color.CYAN), "-" * self.line_length)
        print("")
        return self

    def info(self, *args):
        """Blue text indicating the progress of an operation."""
        self._log(ansi(Color.BLUE), *args)
        return self

    def info2(self, *args):
        """Blue text indicating the progress of an operation."""
        self._log(ansi(Color.CYAN), *args)
        return self
    
    def error(self, *args):
        """Red text indicating an error that is not fatal."""
        self._log(ansi(Color.RED), *args)
        return self

    def warn(self, *args):
        """Yellow text indicating a warning that is not fatal."""
        self._log(ansi(Color.YELLOW), *args)
        return self

    # def warning(self, *args):
    #     self.warn(*args)
    #     self.warn("warn() is recommended over warning().")
    #     return self

    def __call__(self, *args):
        """Display the arguments in blue."""
        self.info(*args)
        return self

    @staticmethod
    def get_caller_info():
        stack = inspect.stack()

        # 0: get_caller_info, 1: log.get_caller_info, 2: caller
        if len(stack) < 3:
            return "Unknown caller"
        
        frame = stack[2]
        frame_info = inspect.getframeinfo(frame[0])

        return {
            "filename": os.path.basename(frame_info.filename),
            "lineno": frame_info.lineno,
            "function": frame_info.function,
            # "code_context": frame_info.code_context
        }

    # あんまり便利じゃない 
    # `log(" " * len(path) + "/".join(path))`とかのほうがシンプルでよい
    # デコレーターとして使えるなら便利かも
    @contextlib.contextmanager
    def indented(self):
        # caller_function = inspect.stack()[2].function
        self.increase()
        # self.header(f"Start {caller_function}")
        try:
            yield
        finally:
            # self._log(CONSOLE_COLOR_CYAN, f"End {caller_function}")
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
    
    def start_timer(self, msg, title=None):
        """Timer start and call header()"""
        self.header("Timer started: " + msg, title)
        self.timer = time.time()
        return self

    def time(self, *args):
        """Display the elapsed time since the timer was started."""
        if self.timer is None:
            self.warn("Timer is not started.")
            return self

        now = time.time()
        self._log(ansi(Color.GREEN), f'{now - self.timer:.4f} sec', *args)
        return self
    
    def stop_timer(self, msg="Timer stopped.", *args):
        """Stop the timer"""
        self.time(msg, *args)
        self.timer = None
        return self


log = PrintLog()

# Usage:
# from debug import log, DBG_HOGE
# DBG_HOGE and log.header("Start processing...").increase()
# for item in data_list:
#     DBG_HOGE and log.info("Processing item:", item, "Status:", process_status)


__all__ = ["log"]
# __all__ += [""]

# Collect all DBG_* flags
__all__ += [name for name in globals() if name.startswith("DBG")]


if __name__ == "__main__":
    pass
