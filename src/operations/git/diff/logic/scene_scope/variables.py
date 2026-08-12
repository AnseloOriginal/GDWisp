from src.operations.git.diff.logic.per_type import variable_diff
from src.operations.project.types import LayoutData

def diff_scene_variables(source: LayoutData, old: LayoutData | None):
    return variable_diff(
      source["variables"],
      old["variables"] if old else None,
    )