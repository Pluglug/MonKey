import bpy
from ..debug import log, DBG_OPS
from .dopesheet_helper import get_visible_objects, get_selected_keyframes


# Keyframe selection moving operators

class GRAPH_OT_monkey_horizontally(bpy.types.Operator):
    bl_idname = "graph.monkey_horizontally"
    bl_label = "Move Keyframe Selection Horizontally"
    bl_options = {'REGISTER', 'UNDO'}

    direction: bpy.props.EnumProperty(  # type: ignore
        name="Direction",
        items=[
            ("forward", "Forward", ""),
            ("backward", "Backward", "")
        ],
        default="forward"
    )
    extend: bpy.props.BoolProperty(default=False)  # type: ignore

    @classmethod
    def poll(cls, context):
        return context.area.type == 'GRAPH_EDITOR'
        # if context.area.type != 'GRAPH_EDITOR':
        #     return False

        # dopesheet = context.space_data.dopesheet
        # visible_objects = get_visible_objects(dopesheet)
        # return bool(visible_objects)  # チェックが完全でないし、操作時混乱する。

    def execute(self, context):
        dopesheet = context.space_data.dopesheet
        visible_objects = get_visible_objects(dopesheet)
        if not visible_objects:
            self.report({'ERROR'}, "There is no object that is displayed and has an action.")
            return {'CANCELLED'}

        move_keyframe_selection_horizontally(self.direction, self.extend, visible_objects)
        return {'FINISHED'}


class GRAPH_OT_monkey_vertically(bpy.types.Operator):
    bl_idname = "graph.monkey_vertically"
    bl_label = "Move Channel Selection Vertically"
    bl_options = {'REGISTER', 'UNDO'}

    direction: bpy.props.EnumProperty(  # type: ignore
        name="Direction",
        items=[
            ("upward", "Upward", ""),
            ("downward", "Downward", "")
        ],
        default="downward"
    )
    extend: bpy.props.BoolProperty(default=False)  # type: ignore

    @classmethod
    def poll(cls, context):
        return context.area.type == 'GRAPH_EDITOR'
        # if context.area.type != 'GRAPH_EDITOR':
        #     return False

        # dopesheet = context.space_data.dopesheet
        # visible_objects = get_visible_objects(dopesheet)
        # return bool(visible_objects)

    def execute(self, context):
        dopesheet = context.space_data.dopesheet
        visible_objects = get_visible_objects(dopesheet)
        if not visible_objects:
            self.report({'ERROR'}, "There is no object that is displayed and has an action.")
            return {'CANCELLED'}
        
        move_channel_selection_vertically(self.direction, self.extend, visible_objects)
        return {'FINISHED'}


# Helper functions

def move_keyframe_selection_horizontally(direction="forward", extend=False, visible_objects=None):
    if visible_objects is None:
        return

    for obj in visible_objects:
        selected_channels = [fcurve for fcurve in obj.animation_data.action.fcurves if fcurve.select]

        if selected_channels:
            process_keyframe_selection_for_horizontal_move(obj, direction, extend)


def process_keyframe_selection_for_horizontal_move(obj, direction="forward", extend=False):
    if direction not in ("forward", "backward"):
        raise ValueError("Invalid value for direction. Must be 'forward' or 'backward'.")

    action = obj.animation_data.action

    for fcurve in action.fcurves:
        if not fcurve.select:  # Only process selected fcurves
            continue

        selected = get_selected_keyframes(fcurve.keyframe_points)

        if not selected:
            continue

        if direction == "forward":
            selected.sort(key=lambda k: k["keyframe"].co[0], reverse=True)
        else:  # direction == "backward"
            selected.sort(key=lambda k: k["keyframe"].co[0])

        for item in selected:
            keyframe = item["keyframe"]
            if direction == "forward":
                target_frame = keyframe.co[0] + 1
            else:  # direction == "backward"
                target_frame = keyframe.co[0] - 1

            next_keyframe = binary_search_keyframe(fcurve, target_frame, direction)

            if next_keyframe is not None:
                transfer_keyframe_selection([item], [next_keyframe], extend)


def binary_search_keyframe(fcurve, target_frame, direction="forward"):
    left = 0
    right = len(fcurve.keyframe_points) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_frame = fcurve.keyframe_points[mid].co[0]

        if mid_frame == target_frame:
            return fcurve.keyframe_points[mid]
        elif mid_frame < target_frame:
            left = mid + 1
        else:
            right = mid - 1

    if direction == "forward" and left < len(fcurve.keyframe_points):
        return fcurve.keyframe_points[left]
    elif direction == "backward" and right >= 0:
        return fcurve.keyframe_points[right]

    return None


def move_channel_selection_vertically(direction="downward", extend=False, visible_objects=None):
    if direction not in ("downward", "upward"):
        raise ValueError("Invalid value for direction. Must be 'downward' or 'upward'.")

    if visible_objects is None:
        return

    all_fcurves = []

    for obj in visible_objects:
        action = obj.animation_data.action
        all_fcurves.extend(action.fcurves)

    num_fcurves = len(all_fcurves)

    selected_indices = [i for i, fcurve in enumerate(all_fcurves) if fcurve.select]

    if direction == "downward":
        selected_indices.sort(reverse=True)
    else:  # direction == "upward"
        selected_indices.sort()

    for current_index in selected_indices:
        fcurve = all_fcurves[current_index]

        if direction == "downward":
            next_index = current_index + 1
        else:  # direction == "upward"
            next_index = current_index - 1

        if 0 <= next_index < num_fcurves:
            next_fcurve = all_fcurves[next_index]
            process_keyframe_selection_for_vertical_move(fcurve, next_fcurve, extend)


def process_keyframe_selection_for_vertical_move(fcurve_from, fcurve_to, extend=False):
    selected = get_selected_keyframes(fcurve_from.keyframe_points)

    if not extend:
        fcurve_from.select = False

    fcurve_to.select = True

    # Move the selection to the nearest keyframes in the new channel
    for item in selected:
        target_keyframes = [
            min(fcurve_to.keyframe_points, key=lambda k: abs(k.co[0] - item["keyframe"].co[0]))
            for item in selected
        ]

        transfer_keyframe_selection(selected, target_keyframes, extend)


def transfer_keyframe_selection(selected, target_keyframes, extend=False):
    for item, target_keyframe in zip(selected, target_keyframes):
        keyframe = item["keyframe"]

        if not extend:
            keyframe.select_control_point = False
        target_keyframe.select_control_point = item["control_point"]

        if keyframe.interpolation == 'BEZIER' and target_keyframe.interpolation == 'BEZIER':
            if item["left_handle"]:
                target_keyframe.select_left_handle = True
                if not extend:
                    keyframe.select_left_handle = False
            if item["right_handle"]:
                target_keyframe.select_right_handle = True
                if not extend:
                    keyframe.select_right_handle = False