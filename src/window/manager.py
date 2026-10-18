import os

import customtkinter
from src.window.view import View_Manager
from typing import TYPE_CHECKING
from src.window.types import VIEW_TYPE, ManagedWindow
from typing import TypedDict
from uuid import uuid4
from src.core.paths import get_asset_path

class Manager:
  """Manages windows"""
  app_window_list: list[ManagedWindow] = []
  
  def __init__(self) -> None:
    root = customtkinter.CTk()
    root.withdraw()
    customtkinter.FontManager.load_font(
      get_asset_path(os.path.join("fonts","Inter-Regular.ttf"))
    )
    self.root = root
    self.view = View_Manager(self)

  def new_window(self, window_type: VIEW_TYPE ,*extras):
    id = uuid4().__str__()
    window = customtkinter.CTkToplevel(self.root)
    window.geometry("800x600")
    update = self.view.create_gui(window,window_type,*extras)
    win: ManagedWindow = {
      "window_type": window_type,
      "update": update,
      "window": window,
      "id": id
    }
    self.app_window_list.append(win)
    # window.bind("<Destroy>", lambda event: self,self.remove_window(id))
  
  def mainloop(self):
    self.root.mainloop()
  
  def close_all(self):
    self.root.quit()

  def remove_window(self,id: str):
    for window in self.app_window_list:
      if (window["id"] == id):
        self.app_window_list.remove(window)
  
  def update_all(self,window_type: VIEW_TYPE):
    for window in self.app_window_list:
      if window["window_type"] == window_type:
        window["update"]()
