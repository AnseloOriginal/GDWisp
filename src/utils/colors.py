import colorsys
from src.operations.project.types import CommentEventColorData

def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"

def string_to_comment_color(text: str) -> CommentEventColorData:
    a = text.replace(" ",";").split(";")
    return {
        "r": int(a[0]),
        "g": int(a[1]),
        "b": int(a[2]),
        "textR": int(a[3]),
        "textG": int(a[4]),
        "textB": int(a[5])
    }

def comment_color_to_string(color: CommentEventColorData):
    return f"{color["r"]};{color["g"]};{color["b"]} {color["textR"]};{color["textG"]};{color["textB"]}"


def color_to_str(r: int, g: int, b: int):
    return f"{r}; {g}; {b}"

def generate_unique_color(i: int):
        golden_ratio_conjugate = 0.618033988749895
        h = (i * golden_ratio_conjugate) % 1.0
        s = 0.85
        v = 0.90
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"