import bpy
import os
# import sys
# import traceback


VERSION = None
BL_VERSION = None
ADDON_ID = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
ADDON_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))


def uprefs():
    return getattr(bpy.context, "preferences", None)

def prefs():
    return uprefs().addons[ADDON_ID].preferences

def since_4_0_0():
    return VERSION >= (4, 0, 0)
