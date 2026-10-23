import tkinter as tk
import os
import sys
import customtkinter
from src.window.view import View_Manager
from src.window.types import VIEW_TYPE, ManagedWindow
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
    self.root.after(300,lambda: self.set_icon(window))
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

  def set_icon(self,window: customtkinter.CTkToplevel):
    print("Starting the icon process for this",str(window))
    # base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    png_path = get_asset_path(os.path.join("images", "logo.png"))
    ico_path = get_asset_path(os.path.join("images", "logo.ico"))
    if sys.platform.startswith("win") and os.path.exists(ico_path):
        window.iconbitmap(ico_path)
        print("windows ICON set:",str(ico_path))
    else:
        icon = tk.PhotoImage(file=png_path)
        window.iconphoto(True, icon)
        window._icon_ref = icon # pyright: ignore[reportAttributeAccessIssue]