import customtkinter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from modules.window.views.view import GUI_Functions
  from modules.operations.git.diff import Diff

def view(app: customtkinter.CTkToplevel, funcs: "GUI_Functions", name: str, location: str, diff: "Diff"):
  app.title("Gdevelop Project: "+name)
  app.geometry("900x600")
  def update():
    pass
  return update