import bpy
from . debug import log, DBG_PREFS

from . addon import ADDON_ID

from . operators.keyframe_moving import GRAPH_OT_monkey_horizontally, GRAPH_OT_monkey_vertically
from . operators.handle_selection import GRAPH_OT_monkey_handle_selecter


class MonKeyPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_ID

    forward_key: bpy.props.StringProperty(name="Forward Key", default="D")
    forward_key_extend: bpy.props.StringProperty(name="Forward Key (Extend)", default="D")
    backward_key: bpy.props.StringProperty(name="Backward Key", default="A")
    backward_key_extend: bpy.props.StringProperty(name="Backward Key (Extend)", default="A")
    upward_key: bpy.props.StringProperty(name="Upward Key", default="W")
    upward_key_extend: bpy.props.StringProperty(name="Upward Key (Extend)", default="W")
    downward_key: bpy.props.StringProperty(name="Downward Key", default="S")
    downward_key_extend: bpy.props.StringProperty(name="Downward Key (Extend)", default="S")

    # def draw(self, context):
    #     layout = self.layout
    #     layout.label(text="Key Bindings:")

    #     col = layout.column(align=True)
    #     col.prop(self, "upward_key")
    #     col.prop(self, "upward_key_extend")

    #     col = layout.column(align=True)
    #     col.prop(self, "forward_key")
    #     col.prop(self, "forward_key_extend")

    #     col = layout.column(align=True)
    #     col.prop(self, "backward_key")
    #     col.prop(self, "backward_key_extend")

    #     col = layout.column(align=True)
    #     col.prop(self, "downward_key")
    #     col.prop(self, "downward_key_extend")


addon_keymaps = []


def register_keymaps():
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Graph Editor', space_type='GRAPH_EDITOR')

    preferences = bpy.context.preferences.addons[__name__].preferences

    # Upward
    kmi = km.keymap_items.new(GRAPH_OT_monkey_vertically.bl_idname, type=preferences.upward_key, value='PRESS', alt=True)
    kmi.properties.direction = "upward"
    kmi.properties.extend = False

    # Upward Extend
    kmi = km.keymap_items.new(GRAPH_OT_monkey_vertically.bl_idname, type=preferences.upward_key_extend, value='PRESS', alt=True, shift=True)
    kmi.properties.direction = "upward"
    kmi.properties.extend = True

    # Downward
    kmi = km.keymap_items.new(GRAPH_OT_monkey_vertically.bl_idname, type=preferences.downward_key, value='PRESS', alt=True)
    kmi.properties.direction = "downward"
    kmi.properties.extend = False

    # Downward Extend
    kmi = km.keymap_items.new(GRAPH_OT_monkey_vertically.bl_idname, type=preferences.downward_key_extend, value='PRESS', alt=True, shift=True)
    kmi.properties.direction = "downward"
    kmi.properties.extend = True

    # Forward
    kmi = km.keymap_items.new(GRAPH_OT_monkey_horizontally.bl_idname, type=preferences.forward_key, value='PRESS', alt=True)
    kmi.properties.direction = "forward"
    kmi.properties.extend = False

    # Forward Extend
    kmi = km.keymap_items.new(GRAPH_OT_monkey_horizontally.bl_idname, type=preferences.forward_key_extend, value='PRESS', alt=True, shift=True)
    kmi.properties.direction = "forward"
    kmi.properties.extend = True

    # Backward
    kmi = km.keymap_items.new(GRAPH_OT_monkey_horizontally.bl_idname, type=preferences.backward_key, value='PRESS', alt=True)
    kmi.properties.direction = "backward"
    kmi.properties.extend = False

    # Backward Extend
    kmi = km.keymap_items.new(GRAPH_OT_monkey_horizontally.bl_idname, type=preferences.backward_key_extend, value='PRESS', alt=True, shift=True)
    kmi.properties.direction = "backward"
    kmi.properties.extend = True

    # Left
    kmi = km.keymap_items.new(GRAPH_OT_monkey_handle_selecter.bl_idname, type='Q', value='PRESS', alt=True)
    kmi.properties.handle_direction = "Left"
    kmi.properties.extend = False

    # Left Extend
    kmi = km.keymap_items.new(GRAPH_OT_monkey_handle_selecter.bl_idname, type='Q', value='PRESS', alt=True, shift=True)
    kmi.properties.handle_direction = "Left"
    kmi.properties.extend = True

    # Right
    kmi = km.keymap_items.new(GRAPH_OT_monkey_handle_selecter.bl_idname, type='E', value='PRESS', alt=True)
    kmi.properties.handle_direction = "Right"
    kmi.properties.extend = False

    # Right Extend
    kmi = km.keymap_items.new(GRAPH_OT_monkey_handle_selecter.bl_idname, type='E', value='PRESS', alt=True, shift=True)
    kmi.properties.handle_direction = "Right"
    kmi.properties.extend = True

    addon_keymaps.append(km)


def unregister_keymaps():
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()