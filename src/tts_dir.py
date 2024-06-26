import os
import sys

import pythoncom


def try_and_find_save_games_folder():
    if sys.platform != "win32":
        return None

    try:
        import win32com.client
    except ImportError:
        return None

    obj_shell = win32com.client.Dispatch("WScript.Shell", pythoncom.CoInitialize())
    docs = (
        obj_shell.SpecialFolders("MyDocuments") + "\My Games\Tabletop Simulator\Saves"
    )

    if os.path.isdir(docs):
        return docs

    return None
