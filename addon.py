import bpy
import os
# import sys
import traceback
import warnings
from .debug import log

VERSION = None
BL_VERSION = None
ADDON_ID = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
ADDON_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


def get_user_preferences(context=bpy.context):
    preferences = getattr(context, "preferences", None)
    if preferences is not None:
        return preferences
    else:
        raise AttributeError("Unable to access preferences")


def get_addon_preferences(context=bpy.context):
    user_prefs = get_user_preferences(context)
    addon_prefs = user_prefs.addons.get(ADDON_ID)
    if addon_prefs is not None:
        return addon_prefs.preferences
    else:
        raise KeyError(f"Addon '{ADDON_ID}' not found. Ensure it is installed and enabled.")


def uprefs():
    caller = traceback.extract_stack(None, 2)[0]  # Get the caller of this function
    warnings.warn(
        f"uprefs() is deprecated. Use get_addon_preferences() instead. Called from {caller.filename}, line {caller.lineno}",
        DeprecationWarning,
        stacklevel=2
    )  # I don't really understand how this module works.
    return get_addon_preferences()


def prefs():
    caller = traceback.extract_stack(None, 2)[0]
    log.warn(f"prefs() is deprecated. Use get_addon_preferences() instead. Called from {caller.filename}, line {caller.lineno}")
    return get_addon_preferences()
