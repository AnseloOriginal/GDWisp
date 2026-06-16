from typing import TypedDict, Any

class PropertiesDiff(TypedDict):
  old: str | bool | dict | int | list
  new: str | bool | dict | int | list | None
  name: str


