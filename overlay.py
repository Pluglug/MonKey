# pyright: reportInvalidTypeForm=false
import bpy
import blf
import re
from time import time

from addon import prefs, since_4_0_0
from debug import log, DBG_OVLY

OVERLAY_ALIGNMENT_ITEMS = [
    ('TOP', "Top", ""),
    ('TOP_LEFT', "Top Left", ""),
    ('TOP_RIGHT', "Top Right", ""),
    ('BOTTOM', "Bottom", ""),
    ('BOTTOM_LEFT', "Bottom Left", ""),
    ('BOTTOM_RIGHT', "Bottom Right", ""),
]


def blf_size(font_id, size, *args, **kwargs):
    if since_4_0_0():
        blf.size(font_id, size)
    else:
        blf.size(font_id, size, 72)


# TODO: Utilsへ移動
def multiton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


class Timer:
    def __init__(self, duration):
        self.reset(duration)

    def update(self):
        current_time = time()
        elapsed_time = current_time - self.start_time
        self.remaining_time -= elapsed_time
        self.start_time = current_time

        return self.remaining_time <= 0

    def reset(self, duration):
        self.remaining_time = duration
        self.start_time = time()

    def is_finished(self):
        return self.remaining_time <= 0


def calculate_aligned_position(
    width: float, height: float, alignment: str,
    object_width: float, object_height: float, 
    offset_x: int, offset_y: int
) -> tuple[float, float]:
    """
    Calculate the aligned position for an object within a given area based on the alignment and offsets.
    
    Parameters:
        width: The width of the area where the object will be displayed.
        height: The height of the area where the object will be displayed.
        alignment: The object alignment within the area (e.g., 'TOP_LEFT', 'BOTTOM').
        object_width: The width of the object.
        object_height: The height of the object.
        offset_x: The horizontal offset from the aligned position.
        offset_y: The vertical offset from the aligned position.

    Returns:
        A tuple of (x, y) coordinates for the object position.
    """
    if alignment not in OVERLAY_ALIGNMENT_ITEMS:
        raise ValueError(f"Invalid alignment: {alignment}")

    if 'TOP' in alignment:
        y = height - object_height - offset_y
    elif 'BOTTOM' in alignment:
        y = offset_y
    else:  # Center
        y = (height - object_height) / 2

    if 'LEFT' in alignment:
        x = offset_x
    elif 'RIGHT' in alignment:
        x = width - object_width - offset_x
    else:  # Center
        x = (width - object_width) / 2

    return x, y


class OverlayText:
    def __init__(self, text="", font_id=0, size=24, color=(1.0, 1.0, 1.0, 1.0),
                 shadow=True, shadow_color=(0.0, 0.0, 0.0, 1.0),
                 alignment='TOP', offset_x=10, offset_y=10):
        self.text = text
        self.font_id = font_id
        self.size = size
        self.color = color
        self.shadow = shadow
        self.shadow_color = shadow_color
        self.alignment = alignment
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.timer = Timer(0.0)


class DrawingSpace:
    def __init__(self, space_type):
        self.space_type = space_type
        self.overlay_text = OverlayText()
        self.handler = None
        self.text_lines = []
        self.active = False


drawing_spaces = {}


def add_space(id, space_type_name):
    space_type = getattr(bpy.types, space_type_name, None)
    if not space_type:
        print(f"Space type '{space_type_name}' not found.")
        return

    drawing_spaces[id] = DrawingSpace(space_type)



def _draw_callback(overlay_text):
    pass






class TextOverlaySettings(bpy.types.PropertyGroup):
    show_text: bpy.props.BoolProperty(
        name="Show Text",
        description="Notify selected channel name",
        default=True,
    )
    size: bpy.props.IntProperty(
        name="Font Size", 
        description="Font size",
        default=24, min=10, max=50, 
        options={'SKIP_SAVE'},
        # update=,
    )
    color: bpy.props.FloatVectorProperty(
        name="Color",
        description="Color",
        default=(1.0, 1.0, 1.0, 1.0),
        subtype='COLOR',
        size=4, min=0.0, max=1.0,
    )
    alignment: bpy.props.EnumProperty(
        name="Alignment",
        description="Text alignment on area",
        items=OVERLAY_ALIGNMENT_ITEMS,
        default='TOP',
    )
    duration: bpy.props.FloatProperty(
        name="Duration",
        description="Duration of the text display",
        default=1.0, min=0.0,
    )
    offset_x: bpy.props.IntProperty(
        name="Offset X", description="Offset from area edge",
        subtype='PIXEL', 
        default=10, min=0,
    )
    offset_y: bpy.props.IntProperty(
        name="Offset Y", description="Offset from area edge",
        subtype='PIXEL', 
        default=10, min=0,
    )
    use_shadow: bpy.props.BoolProperty(
        name="Use Shadow",
        description="Use shadow for text",
        default=True,
    )
    shadow_color: bpy.props.FloatVectorProperty(
        name="Shadow Color",
        description="Shadow color",
        default=(0.0, 0.0, 0.0, 1.0),
        subtype='COLOR',
        size=4, min=0.0, max=1.0,
    )
    shadow_blur: bpy.props.IntProperty(
        name="Shadow Blur",
        description="Shadow blur level. can be 3, 5 or 0",
        subtype='PIXEL',
        default=3, min=0, max=5,
    )
    shadow_offset_x: bpy.props.IntProperty(
        name="Shadow Offset X",
        description="Shadow offset from text",
        subtype='PIXEL',
        default=2, min=0,
    )
    shadow_offset_y: bpy.props.IntProperty(
        name="Shadow Offset Y",
        description="Shadow offset from text",
        subtype='PIXEL',
        default=2, min=0,
    )

    def draw(self, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.label(text="Text Overlay Settings")
        # layout.prop(self, "show_text")
        layout.prop(self, "size")
        layout.prop(self, "color")
        layout.prop(self, "alignment")
        layout.prop(self, "duration")
        layout.prop(self, "offset_x")
        layout.prop(self, "offset_y")
        layout.prop(self, "use_shadow")
        layout.prop(self, "shadow_color")
        layout.prop(self, "shadow_blur")
        layout.prop(self, "shadow_offset_x")
        layout.prop(self, "shadow_offset_y")
    

# function to channel info

def convert_data_path_to_readable(channel_data_path: str) -> str:
    DBG_OVLY and log.header(
        f"convert_data_path_to_readable(\n    '{channel_data_path}')")
    replace_list = [
        ('["', ' '), 
        ('"].', ' < '), 
        ('_', ' '), 
        ]
    for old, new in replace_list:
        channel_data_path = channel_data_path.replace(old, new)

    readable_data_path = re.sub(r"(\.)([A-Z])", r"\1 \2", channel_data_path)
    readable_data_path = ' '.join(word.capitalize() for word in readable_data_path.split(' '))

    DBG_OVLY and log(f"readable_data_path: {readable_data_path}")
    return readable_data_path


def gen_channel_info_line(obj, fcurve):
    show = prefs().overlay.info_to_display

    info_str = ""
    if show.object_name:
        info_str += f"< {obj.name} >"
    if show.action_name:
        info_str += f"< {fcurve.id_data.name} >"
    if fcurve.group and show.group_name:
        info_str += f"< {fcurve.group.name} >"
    if show.channel_name:
        info_str += f" {convert_data_path_to_readable(fcurve.data_path)} >"

    info_str = info_str.replace("><", "|")

    DBG_OVLY and log(f"channel_info_line: {info_str}")
    return info_str



# def get_channel_info(visible_objects):
#     selected_channels = [(obj, fcurve) for obj in visible_objects for fcurve in obj.animation_data.action.fcurves if fcurve.select]

#     # Only display info if a single channel is selected
#     if len(selected_channels) == 1:
#         show = prefs().overlay.info_to_display
#         obj, fcurve = selected_channels[0]
#         object_name = obj.name if show.object_name else None
#         action_name = fcurve.id_data.name if show.action_name else None
#         group_name = fcurve.group.name if fcurve.group and show.group_name else None
#         channel_name = convert_data_path_to_readable(fcurve.data_path) if show.channel_name else None

#         info_str = ""
#         if object_name:
#             info_str += f"< {object_name} >"
#         if action_name:
#             info_str += f"< {action_name} >"
#         if group_name:
#             info_str += f"< {group_name} >"
#         if channel_name:
#             info_str += f" {channel_name} >"
        
#         info_str = info_str.replace("><", "|")
        
#         return info_str
#     return None


class ChannelInfoToDisplay(bpy.types.PropertyGroup):
    object_name: bpy.props.BoolProperty(
        name="Object Name",
        description="Display object name",
        default=True,
    )
    action_name: bpy.props.BoolProperty(
        name="Action Name",
        description="Display action name",
        default=True,
    )
    group_name: bpy.props.BoolProperty(
        name="Group Name",
        description="Display group name",
        default=True,
    )
    channel_name: bpy.props.BoolProperty(
        name="Channel Name",
        description="Display channel name",
        default=True,
    )

    def draw(self, layout):
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.label(text="Channel Info to Display")
        layout.prop(self, "object_name")
        layout.prop(self, "action_name")
        layout.prop(self, "group_name")
        layout.prop(self, "channel_name")




class TextDisplayHandler:
    def __init__(self):
        self.draw_handler = None

    def start(self, context):
        if self.draw_handler is None:
            self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(
                self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')

    def stop(self):
        if self.draw_handler is not None:
            bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')
            self.draw_handler = None

    def is_active(self):
        return self.draw_handler is not None
    
    def draw_callback(self, context):
        pr = prefs()

        # Generate the text lines based on the current context
        text_lines = generate_text_lines(context)

        # Check if text should be displayed
        if not pr.show_text or not text_lines:
            return

        font_id = 0
        blf_size(font_id, pr.text_size)  # Set font size from addon preferences
        blf.color(font_id, *pr.text_color)  # Set text color from addon preferences

        # Get the initial value of y_offset
        y_offset = pr.overlay_offset_y
        
        for text in text_lines:
            # Get the screen position for the text based on the alignment
            x, y = get_screen_position(context, text, pr.overlay_alignment, pr.overlay_offset_x, y_offset, font_id)

            # Draw the text at the calculated position
            blf.position(font_id, x, y, 0)
            blf.draw(font_id, text)

            # Calculate the height of the text
            text_height = blf.dimensions(font_id, text)[1]

            # Adjust y_offset for the next line depending
            y_offset += (text_height + pr.line_offset)


text_display_handler = TextDisplayHandler()


class TEXT_OT_activate_handler(bpy.types.Operator):
    """Activate the text display handler"""
    bl_idname = "text.activate_handler"
    bl_label = "Activate Text Handler"

    @classmethod
    def poll(cls, context):
        return not text_display_handler.is_active()

    # @log_exec
    def execute(self, context):
        text_display_handler.start(context)
        return {'FINISHED'}


class TEXT_OT_deactivate_handler(bpy.types.Operator):
    """Deactivate the text display handler"""
    bl_idname = "text.deactivate_handler"
    bl_label = "Deactivate Text Handler"

    @classmethod
    def poll(cls, context):
        return text_display_handler.is_active()

    # @log_exec
    def execute(self, context):
        text_display_handler.stop()
        return {'FINISHED'}


# def activate_handler():
#     bpy.ops.text.activate_handler()
#     return None  # Stop the timer


# operator_classes = [
#     TEXT_OT_activate_handler,
#     TEXT_OT_deactivate_handler,
# ]

if __name__ == "__main__":
    pass