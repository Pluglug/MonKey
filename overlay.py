import bpy
import blf

from addon import is_40, prefs

from debug import log, log_exec


alignment_items = [
    ('TOP', "Top", ""),
    ('TOP_LEFT', "Top Left", ""),
    ('TOP_RIGHT', "Top Right", ""),
    ('BOTTOM', "Bottom", ""),
    ('BOTTOM_LEFT', "Bottom Left", ""),
    ('BOTTOM_RIGHT', "Bottom Right", ""),
]


def blf_size(font_id, size):
    if is_40():
        blf.size(font_id, size)
    else:
        blf.size(font_id, size, 72)


def get_screen_position(context, text, alignment, offset_x, offset_y, font_id=0):
    # Determine the x, y position based on alignment
    region = context.region
    width, height = region.width, region.height

    text_width, text_height = blf.dimensions(font_id, text)
    
    if 'TOP' in alignment:
        y = height - text_height - offset_y
    elif 'BOTTOM' in alignment:
        y = offset_y
    else:
        # Center vertically if neither TOP nor BOTTOM
        y = (height - text_height) / 2

    if 'LEFT' in alignment:
        x = offset_x
    elif 'RIGHT' in alignment:
        x = width - text_width - offset_x
    else:
        # Center horizontally if neither LEFT nor RIGHT
        x = (width - text_width) / 2  # + offset_x

    return (x, y)


# class TextDisplayHandler:
#     def __init__(self):
#         self.draw_handler = None

#     def start(self, context):
#         if self.draw_handler is None:
#             self.draw_handler = bpy.types.SpaceView3D.draw_handler_add(
#                 self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')

#     def stop(self):
#         if self.draw_handler is not None:
#             bpy.types.SpaceView3D.draw_handler_remove(self.draw_handler, 'WINDOW')
#             self.draw_handler = None

#     def is_active(self):
#         return self.draw_handler is not None
    
#     def draw_callback(self, context):
#         pr = prefs()

#         # Generate the text lines based on the current context
#         text_lines = generate_text_lines(context)

#         # Check if text should be displayed
#         if not pr.show_text or not text_lines:
#             return

#         font_id = 0
#         blf_size(font_id, pr.text_size)  # Set font size from addon preferences
#         blf.color(font_id, *pr.text_color)  # Set text color from addon preferences

#         # Get the initial value of y_offset
#         y_offset = pr.overlay_offset_y
        
#         for text in text_lines:
#             # Get the screen position for the text based on the alignment
#             x, y = get_screen_position(context, text, pr.overlay_alignment, pr.overlay_offset_x, y_offset, font_id)

#             # Draw the text at the calculated position
#             blf.position(font_id, x, y, 0)
#             blf.draw(font_id, text)

#             # Calculate the height of the text
#             text_height = blf.dimensions(font_id, text)[1]

#             # Adjust y_offset for the next line depending
#             y_offset += (text_height + pr.line_offset)


# text_display_handler = TextDisplayHandler()


# class TEXT_OT_activate_handler(bpy.types.Operator):
#     """Activate the text display handler"""
#     bl_idname = "text.activate_handler"
#     bl_label = "Activate Text Handler"

#     @classmethod
#     def poll(cls, context):
#         return not text_display_handler.is_active()

#     @log_exec
#     def execute(self, context):
#         text_display_handler.start(context)
#         return {'FINISHED'}


# class TEXT_OT_deactivate_handler(bpy.types.Operator):
#     """Deactivate the text display handler"""
#     bl_idname = "text.deactivate_handler"
#     bl_label = "Deactivate Text Handler"

#     @classmethod
#     def poll(cls, context):
#         return text_display_handler.is_active()

#     @log_exec
#     def execute(self, context):
#         text_display_handler.stop()
#         return {'FINISHED'}


# def activate_handler():
#     bpy.ops.text.activate_handler()
#     return None  # Stop the timer


# operator_classes = [
#     TEXT_OT_activate_handler,
#     TEXT_OT_deactivate_handler,
# ]

if __name__ == "__main__":
    pass