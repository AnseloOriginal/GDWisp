from pathlib import Path
from PIL import Image


LOGO_IMAGE_PATH = Path(__file__).resolve().parents[2] / "images" / "logo.png"

logo_image = Image.open(LOGO_IMAGE_PATH)