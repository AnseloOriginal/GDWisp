from typing import Literal,TypedDict,Callable
from customtkinter import CTkToplevel

VIEW_TYPE = Literal["Main", "Error", "Project", "Settings"]

class ManagedWindow(TypedDict):
  window: CTkToplevel
  window_type: VIEW_TYPE
  update: Callable
  id: str