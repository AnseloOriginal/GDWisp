from typing import Literal

from src.operations.git.diff.types import OldNewDiff
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

def old_new_extractor(type: Literal["new","old"], ondiff: OldNewDiff | str) -> str | None:
    if isinstance(ondiff,str):
        return ondiff
    target = ondiff[type]
    return target if isinstance(target,str) else None
