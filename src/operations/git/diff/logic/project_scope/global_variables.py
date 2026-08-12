from src.operations.git.diff.logic.per_type import variable_diff
from src.operations.project.types import ProjectData


def global_variable_diff(current: ProjectData, old: ProjectData | None):
  return variable_diff(
    current["variables"],
    old["variables"] if old else None
  )