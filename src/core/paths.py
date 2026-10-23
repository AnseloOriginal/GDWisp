from platformdirs import user_data_path
import os
import sys

def get_asset_path(relative_path: str):
    """Get absolute path to resource, works for dev and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

folder_path = user_data_path(appname="GDWisp", appauthor=False, ensure_exists=True, roaming=True)
print(f"[DEBUG] GDWisp folder initialized at: {folder_path.resolve()}")


