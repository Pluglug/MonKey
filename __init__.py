import bpy
# import bpy_extras

from . debug import log, DBG_INIT
from . import addon

bl_info = {
    "name": "MonKey",
    "author": "Pluglug",
    "version": (0, 6, 0),
    "blender": (2, 80, 0),
    "location": "Graph Editor",
    "description": "Move keyframe selection in the Graph Editor",
    "warning": "It'll explode",
    "wiki_url": "",
    "category": "Animation",
}

addon.VERSION = bl_info["version"]
addon.BL_VERSION = bl_info["blender"]

from . operators.keyframe_moving import GRAPH_OT_monkey_horizontally, GRAPH_OT_monkey_vertically
from . operators.handle_selection import GRAPH_OT_monkey_handle_selecter
from . preferences import MonKeyPreferences
from . keymap import register_keymaps, unregister_keymaps

classes = (
    GRAPH_OT_monkey_horizontally,
    GRAPH_OT_monkey_vertically,
    GRAPH_OT_monkey_handle_selecter,
    MonKeyPreferences,
)


def register():
    DBG_INIT and log.header("Registering MonKey", "INIT")
    DBG_INIT and log.info("Version: " + str(addon.VERSION))
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    # bpy.types.Scene.monkey_preferences = bpy.props.PointerProperty(type=MonKeyPreferences)
    register_keymaps()

def unregister():
    DBG_INIT and log.header("Unregistering MonKey", "INIT")
    unregister_keymaps()
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    # del bpy.types.Scene.monkey_preferences

if __name__ == "__main__":
    pass
