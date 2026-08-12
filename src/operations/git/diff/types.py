from typing import Literal, TypedDict, Any

type OldType = str | bool | dict | int | list | float| None
type NewType = str | bool | dict | int | list | float| None
type ActionType = Literal["Modified", "Created", "Deleted"]
class OldNewDiff(TypedDict):
  old: OldType
  new: NewType
  name: str


class VariableDiff(TypedDict):
  name: str
  var_type: OldNewDiff | None
  default: OldNewDiff | None
  change: ActionType

class LayerDiff(TypedDict):
  name: str
  change: ActionType
  diff: list[OldNewDiff] | None

class InstanceDiff(TypedDict):
  change: ActionType
  diff: list[OldNewDiff] | None
  object_name: str

class SceneDiff(TypedDict):
  properties: list[OldNewDiff] | None
  variables: list[VariableDiff] | None
  layers: list[LayerDiff] | None
  instances: list[InstanceDiff] | None