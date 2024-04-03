import bpy
# import rna_keymap_ui
from rna_keymap_ui import draw_kmi

from . debug import log, DBG_PREFS

from . addon import ADDON_ID

from . operators.keyframe_moving import GRAPH_OT_monkey_horizontally, GRAPH_OT_monkey_vertically
from . operators.handle_selection import GRAPH_OT_monkey_handle_selecter

ops_idnames = [
    GRAPH_OT_monkey_horizontally.bl_idname,
    GRAPH_OT_monkey_vertically.bl_idname,
    GRAPH_OT_monkey_handle_selecter.bl_idname,
]

class MonKeyPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_ID

    def draw(self, context):
        layout = self.layout

        self.draw_keymap(layout)
    
    def draw_keymap(self, layout):
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon
        km = kc.keymaps.get('Graph Editor')

        if not km:
            return
        
        layout.label(text="MonKey Keymap")

        for kmi in km.keymap_items:
            if kmi.idname in ops_idnames:
                draw_kmi([], kc, km, kmi, layout, 0)
                layout.separator()

# del ops_idnames
# del GRAPH_OT_monkey_horizontally
# del GRAPH_OT_monkey_vertically
# del GRAPH_OT_monkey_handle_selecter
