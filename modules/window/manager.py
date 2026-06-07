import customtkinter
from modules.window.views.view import View_Manager
from typing import TYPE_CHECKING
from modules.window.types import VIEW_TYPE, ManagedWindow
from typing import TypedDict

class Manager:
  """Manages windows"""
  app_window_list: list[ManagedWindow] = []
  
  def __init__(self) -> None:
    root = customtkinter.CTk()
    root.withdraw()
    self.root = root
    self.view = View_Manager(self)

  def new_window(self, window_type: VIEW_TYPE ,*extras):
    window = customtkinter.CTkToplevel(self.root)
    window.geometry("800x600")
    update = self.view.create_gui(window,window_type,*extras)
    win: ManagedWindow = {
      "window_type": window_type,
      "update": update,
      "window": window
    }
    self.app_window_list.append(win)
    # window.bind("<Destroy>", lambda event: self,self.remove_window(window))
  
  def mainloop(self):
    self.root.mainloop()
  
  def close_all(self):
    self.root.quit()

  def remove_window(self,window: ManagedWindow):
    if window in self.app_window_list:
      self.app_window_list.remove(window)
  
  def update_all(self,window_type: VIEW_TYPE):
    for window in self.app_window_list:
      if window["window_type"] == window_type:
        window["update"]()
