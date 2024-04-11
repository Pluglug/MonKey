from typing import Any
import bpy
from time import time


# bl_info = {
#     "name": "Hold Test",
#     "description": "Hotkey to call a menu after holding the key for a certain duration",
#     "author": "Pluglug",
#     "version": (0, 0, 1),
#     "blender": (2, 9, 0),
#     "location": "View3D > Object > Press alt+Q",
#     "warning": "It'll explode",
#     "wiki_url": "",
#     "category": "Development" 
# }


class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        if self._start_time is not None:
            raise RuntimeError("Timer is already running.")
        self._start_time = time.time()

    def elapsed(self):
        if self._start_time is None:
            raise RuntimeError("Timer has not been started.")
        return time.time() - self._start_time

    def reset(self):
        self._start_time = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed()
        self.reset()


class OBJECT_OT_call_my_menu(bpy.types.Operator):
    bl_idname = "object.call_my_menu"
    bl_label = "Call My Menu"
    bl_description = "Call a menu after holding the key for a certain duration"
    # bl_options = {'INTERNAL'}
    
    hold_time: bpy.props.FloatProperty(
        name="Hold Time", 
        default=2.0
    )

    _timer : Timer = None

    def modal(self, context, event):
        if event.type == 'Q' and event.value == 'RELEASE':
            Log.info("Key released")

            if self._timer.elapsed() >= self.hold_time:
                bpy.ops.wm.call_menu(name="OBJECT_MT_my_hold_menu")
                Log.info("Menu called")
            self.cancel(context)
            Log.footer("Modal finished")
            # return {'FINISHED'}
            return {'CANCELLED'}

        if self._timer.elapsed() >= self.hold_time:
            Log.info("Key held")
            # Do something if the key is held for the duration
            pass

        return {'RUNNING_MODAL'}

    def execute(self, context):
        Log.error("This operator should be called as a modal operator")
        return {'CANCELLED'}

    def invoke(self, context, event):
        Log.header("Invoke", "INIT")
        self._timer = Timer()
        self._timer.start()
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        if self._timer:
            del self._timer
            Log.info("Timer deleted")


class OBJECT_MT_my_hold_menu(bpy.types.Menu):
    bl_label = "Hold menu"
    bl_idname = "OBJECT_MT_my_hold_menu"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Menu called by Hold")


class OBJECT_MT_my_menu(bpy.types.Menu):
    bl_label = "My Menu"
    bl_idname = "OBJECT_MT_my_menu"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Normal menu not caused by Hold")


classes = (
    OBJECT_OT_call_my_menu,
    OBJECT_MT_my_hold_menu,
    OBJECT_MT_my_menu
)


addon_keymaps = []

def _keymap() -> list:
    keymap = []

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')

    # Order is important!

    kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS', alt=True)
    kmi.properties.name = "OBJECT_MT_my_menu_normal"
    keymap.append((km, kmi))

    kmi = km.keymap_items.new('object.call_my_menu', 'Q', 'PRESS', alt=True)
    keymap.append((km, kmi))

    return keymap


# def register():
#     log.header("Registering Hold Test", "INIT")
#     from bpy.utils import register_class
#     for cls in classes:
#         log.blue("Registering", cls.__name__)
#         register_class(cls)
    
#     addon_keymaps.extend(_keymap())
    
#     log.footer("Hold Test registered")

# def unregister():
#     log.header("Unregistering Hold Test", "INIT")
#     from bpy.utils import unregister_class
#     for cls in reversed(classes):
#         log.blue("Unregistering", cls.__name__)
#         unregister_class(cls)

#     for km, kmi in addon_keymaps:
#         km.keymap_items.remove(kmi)
#     addon_keymaps.clear()

#     log.footer("Hold Test unregistered")


# Logger v2
class Log:
    """Simple Print Logger with colors"""
    class _style:
        # Colors can add 10 and 60
        BLACK = 30
        RED = 31
        GREEN = 32
        YELLOW = 33
        BLUE = 34
        MAGENTA = 35
        CYAN = 36
        WHITE = 37

        # Styles
        BOLD = 1
        FAINT = 2
        ITALIC = 3
        UNDERLINE = 4
        INVERTED = 7
        
        # Reset
        END = 0

    LINE_LENGTH = 50

    @classmethod
    def ansi(cls, *codes):
        return f'\033[{";".join(str(code) for code in codes)}m'

    @classmethod
    def color_print(cls, color, *args):
        msg = ", ".join(str(arg) for arg in args)
        try:
            if isinstance(color, (tuple, list)):
                color_code = cls.ansi(*color)
            else:
                color_code = cls.ansi(color)
            print(f"{color_code}{msg}{cls.ansi(cls._style.END)}")
        except Exception as e:
            try:
                import bpy
                bpy.ops.wm.report({'ERROR'}, message=f"Logging error: {e}")
            except Exception as import_error:
                print(f"Logging error: {import_error}")
    
    @classmethod
    def info(cls, *args):
        cls.color_print(cls._style.BLUE, *args)

    @classmethod
    def warn(cls, *args):
        cls.color_print(cls._style.YELLOW, *args)
    
    warning = warn

    @classmethod
    def error(cls, *args):
        cls.color_print(cls._style.RED, *args)
    
    @classmethod
    def bl_report(cls, *args):
        cls.info(*args)
        try:
            import bpy
            bpy.ops.wm.report({'INFO'}, message=", ".join(str(arg) for arg in args))
        except Exception as import_error:
            cls.error(f"Logging error: {import_error}")

    @classmethod
    def bl_error(cls, *args):
        cls.error(*args)
        try:
            import bpy
            bpy.ops.wm.report({'ERROR'}, message=", ".join(str(arg) for arg in args))
        except Exception as import_error:
            cls.error(f"Logging error: {import_error}")

    @classmethod
    def header(cls, msg=None, title=None):
        print("")
        header_length = cls.LINE_LENGTH if msg is None else max(len(msg), cls.LINE_LENGTH)
        title_text = (title.center(header_length, '-') if title is not None else "-" * header_length)
        cls.color_print((cls._style.GREEN, cls._style.BOLD), title_text)
        if msg:
            cls.color_print((cls._style.BOLD, cls._style.GREEN), msg)
    
    @classmethod
    def footer(cls, *args):
        footer_text = ", ".join(str(arg) for arg in args)
        cls.color_print(cls._style.CYAN, footer_text + "\n" + "-" * cls.LINE_LENGTH)
        print("")


class DebugTimer:
    def __init__(self):
        self._start_time = None
        self._lap_times = []

    def print_time(self, *args):
        color = (
            Log._style.WHITE + 10,  # White background
            Log._style.BOLD
        )
        Log.color_print(color, *args)

    def start(self, msg=None, title=None):
        if self._start_time is not None:
            raise RuntimeError("Timer is already running.")
        self._start_time = time()
        Log.header(msg, title)

    def elapsed(self):
        if self._start_time is None:
            raise RuntimeError("Timer has not been started.")
        return time() - self._start_time

    def reset(self):
        self._start_time = None
        self._lap_times.clear()

    def lap(self, label=None):
        if self._start_time is None:
            raise RuntimeError("Timer has not been started.")
        lap_time = time() - self._start_time
        self._lap_times.append((label, lap_time))
        
        self.print_time(f"Lap {len(self._lap_times)}: {label if label else 'No label'} - {lap_time:.4f} sec ")
        return lap_time

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        elapsed = self.elapsed()
        self.print_time(f"Elapsed time: {elapsed:.4f} sec")
        self.reset()
        return elapsed
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper
    
    @property
    def lap_times(self):
        """Can be used to find sums, averages, minimum maximum values, etc."""
        return self._lap_times
    
    @property
    def total_time(self):
        return sum(t for _, t in self._lap_times)


debug_timer = DebugTimer()


if __name__ == "__main__":
    # DebugTimer Test
    with DebugTimer() as timer:
        timer.lap("Start")
        timer.lap("Middle")
        timer.lap("End")
