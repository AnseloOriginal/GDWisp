from src.operations.git.diff import keys
from src.utils.colors import color_to_str
from src.operations.git.diff import renaming
from src.operations.project.types import LayoutData
from src.operations.git.diff.logic.per_type import old_new_diff


def diff_scene_properties(source: LayoutData, old: LayoutData | None):

  newpluscolor = source | {
    "color": color_to_str(source["r"],source["v"],source["b"]),
  }

  oldpluscolor = old | {
    "color": color_to_str(old["r"],old["v"],old["b"])
  } if old else None

  diff = old_new_diff(
    keys.scene_properties,
    newpluscolor,
    oldpluscolor,
    renaming.scene_properties,
    ["r","v","b"]
  )
  return diff