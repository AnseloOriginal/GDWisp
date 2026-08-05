from typing import Literal, TypedDict, Any

class OldNewDiff(TypedDict):
  old: str | bool | dict | int | list | float| None
  new: str | bool | dict | int | list | float
  name: str


class VariableDiff(TypedDict):
  name: str
  var_type: OldNewDiff | None
  default: OldNewDiff | None
  change: Literal["Modified", "Created", "Deleted"]