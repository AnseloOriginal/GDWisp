from pathlib import Path
from PIL import Image


LOGO_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "logo.png"
ICON_ADD_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "Add.png"
ICON_DIFF_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "diff.png"
ICON_HELP_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "help.png"
ICON_SETTINGS_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "settings.png"
ICON_EXPAND_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "expanded.png"
ICON_CONTRACT_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "contracted.png"
ICON_QUICK_OPEN_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "Quick Open.png"
ICON_RIGHT_ARROW_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "Right Arrow.png"
ICON_BULLET_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "icons" / "BUllet.png"

logo_image = Image.open(LOGO_IMAGE_PATH)

ICON = {
  "add": Image.open(ICON_ADD_IMAGE_PATH),
  "diff": Image.open(ICON_DIFF_IMAGE_PATH),
  "help": Image.open(ICON_HELP_IMAGE_PATH),
  "settings": Image.open(ICON_SETTINGS_IMAGE_PATH),
  "expanded": Image.open(ICON_EXPAND_IMAGE_PATH),
  "contracted": Image.open(ICON_CONTRACT_IMAGE_PATH),
  "open": Image.open(ICON_QUICK_OPEN_IMAGE_PATH),
  "right arrow": Image.open(ICON_RIGHT_ARROW_IMAGE_PATH),
  "bullet": Image.open(ICON_BULLET_IMAGE_PATH)
}

