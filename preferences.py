# pyright: reportInvalidTypeForm=false
import bpy
# import rna_keymap_ui
from rna_keymap_ui import draw_kmi

from . debug import log, DBG_PREFS

from . addon import ADDON_ID

from . operators.keyframe_moving import GRAPH_OT_monkey_horizontally, GRAPH_OT_monkey_vertically
from . operators.handle_selection import GRAPH_OT_monkey_handle_selecter

from . overlay import TextOverlaySettings, ChannelInfoToDisplay

ops_idnames = [
    GRAPH_OT_monkey_horizontally.bl_idname,
    GRAPH_OT_monkey_vertically.bl_idname,
    GRAPH_OT_monkey_handle_selecter.bl_idname,
]

class MonKeyPreferences(bpy.types.AddonPreferences):
    bl_idname = ADDON_ID

    tab: bpy.props.EnumProperty(
        name="Tab",
        description="Tab to open",
        items=[
            ('HowToUse', "How to use", ""),
            ('KEYMAP', "Keymap", ""),
            ('OVERLAY', "Overlay", ""),
        ],
        default='KEYMAP'
    )
    overlay: bpy.props.PointerProperty(type=TextOverlaySettings)
    info_to_display: bpy.props.PointerProperty(type=ChannelInfoToDisplay)


    def draw(self, context):
        layout = self.layout

        layout.prop(self, "tab", expand=True)
        if self.tab == 'HowToUse':
            self.draw_description(layout)
        elif self.tab == 'OVERLAY':
            self.overlay.draw(layout)
        elif self.tab == 'KEYMAP':
            self.draw_keymap(layout)
    
    def draw_description(self, layout):
        layout.label(text="This is a description")
        # TODO: Add description

    def draw_keymap(self, layout):
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps.get('Graph Editor')

        if not km:
            return
        
        layout.label(text="MonKey Keymap")

        for kmi in km.keymap_items:
            if kmi.idname in ops_idnames:
                draw_kmi([], kc, km, kmi, layout, 0)
                # layout.separator()

# del ops_idnames
# del GRAPH_OT_monkey_horizontally
# del GRAPH_OT_monkey_vertically
# del GRAPH_OT_monkey_handle_selecter
