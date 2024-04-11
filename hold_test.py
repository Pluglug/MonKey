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
    def __init__(self, duration):
        self.duration = duration
        self.reset(duration)

    def update(self):
        current_time = time()
        elapsed_time = current_time - self.start_time
        self.remaining_time -= elapsed_time
        self.start_time = current_time
        return self.remaining_time <= 0

    def reset(self, duration=None):
        if duration is not None:
            self.duration = duration
        self.remaining_time = self.duration
        self.start_time = time()

    def elapsed_ratio(self):
        return max(0, min(1, (self.duration - self.remaining_time) / self.duration))

    def is_finished(self):
        return self.remaining_time <= 0


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
            log.yellow("Key released",
                 "Timer finished" if self._timer.is_finished() else "Timer cancelled")
            
            if self._timer.is_finished():
                bpy.ops.wm.call_menu(name="OBJECT_MT_my_hold_menu")
                log.green("Menu called")
            self.cancel(context)
            log.footer("Modal finished")
            # return {'FINISHED'}
            return {'CANCELLED'}

        if self._timer.update():
            log.blue("Timer finished")
            # Do something if the key is held for the duration
            pass

        return {'RUNNING_MODAL'}

    def execute(self, context):
        log.red("Execute called, this should not happen")
        return {'CANCELLED'}

    def invoke(self, context, event):
        log.header("Key pressed", "INVOKED")
        self._timer = Timer(self.hold_time)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        if self._timer:
            del self._timer
            log.yellow("Timer deleted")


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


class log:
    @classmethod
    def _print(cls, color, *args) -> None:  
        msg = ""
        for arg in args:
            if msg:
                msg += ", "
            msg += str(arg)
        print(color + msg + '\033[0m')
    
    @classmethod
    def blue(cls, *args):
        cls._print('\033[34m', *args)

    @classmethod
    def green(cls, *args):
        cls._print('\033[32m', *args)
    
    @classmethod
    def magenta(cls, *args):
        cls._print('\033[35m', *args)
    
    @classmethod
    def red(cls, *args):
        cls._print('\033[31m', *args)

    @classmethod
    def yellow(cls, *args):
        cls._print('\033[33m', *args)

    @classmethod
    def header(cls, msg, title=None):
        print("")
        if title is not None:
            title = str(title)
            header_length = max(len(msg), 50)
            title_text = title.center(header_length, '-')
            cls._print('\033[1;32m', title_text)
        if msg:
            cls._print('\033[1;32m', msg)
    
    @classmethod
    def footer(cls, *args):
        cls._print('\033[36m', *args)
        cls._print('\033[36m', "-" * 50)
        print("")


if __name__ == "__main__":
    pass
