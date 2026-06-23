from typing import TypedDict, Any

class PropertiesDiff(TypedDict):
  old: str | bool | dict | int | list | None
  new: str | bool | dict | int | list
  name: str


