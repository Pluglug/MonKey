import bpy

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

# # reload submodules on addon restart
# if "bpy" in locals():
#     from importlib import reload
#     import sys
#     for mod in sys.modules:  # BUG
#         if mod.startswith(f"{addon.ADDON_ID}."):
#             reload(sys.modules[mod])
#     # reload(addon)
#     # reload(log)
#     # reload(GRAPH_OT_monkey_horizontally)
#     # reload(GRAPH_OT_monkey_vertically)
#     # reload(GRAPH_OT_monkey_handle_selecter)
#     # reload(MonKeyPreferences)
#     # reload(register_keymaps)
#     # reload(unregister_keymaps)

classes = (
    GRAPH_OT_monkey_horizontally,
    GRAPH_OT_monkey_vertically,
    GRAPH_OT_monkey_handle_selecter,
    MonKeyPreferences,
)


def register():
    if bpy.app.background:
        return
    
    if bpy.app.version < addon.BL_VERSION:
        log.error("MonKey requires Blender " + ".".join(map(str, addon.BL_VERSION)) + " or later")
        return

    DBG_INIT and log.header("Registering MonKey", "INIT")
    DBG_INIT and log.info("Version: " + str(addon.VERSION))
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    # bpy.types.Scene.monkey_preferences = bpy.props.PointerProperty(type=MonKeyPreferences)
    register_keymaps()
    # for name, package in module_names:  # TODO: 各モジュールのregisterを呼ぶ
    #     mod = importlib.import_module(name, package)
    #     mod.register()


def unregister():
    if bpy.app.background:
        return

    DBG_INIT and log.header("Unregistering MonKey", "INIT")
    unregister_keymaps()
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    # del bpy.types.Scene.monkey_preferences


if __name__ == "__main__":
    pass
