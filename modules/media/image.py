from pathlib import Path
from PIL import Image


LOGO_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "logo.png"
ICON_ADD_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "Add.png"
ICON_DIFF_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "diff.png"
ICON_HELP_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "help.png"
ICON_SETTINGS_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "settings.png"

logo_image = Image.open(LOGO_IMAGE_PATH)

ICON = {
  "add": Image.open(ICON_ADD_IMAGE_PATH),
  "diff": Image.open(ICON_DIFF_IMAGE_PATH),
  "help": Image.open(ICON_HELP_IMAGE_PATH),
  "settings": Image.open(ICON_SETTINGS_IMAGE_PATH)
}

