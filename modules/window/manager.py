import customtkinter
from . import view

class Manager:
  """Manages windows"""
  app_window_list: list[customtkinter.CTkToplevel] = []
  
  def __init__(self) -> None:
    root = customtkinter.CTk()
    root.withdraw()
    self.root = root

  def new_window(self):
    window = customtkinter.CTkToplevel(self.root)
    window.geometry("800x600")
    view.set_main_view(window)
    self.app_window_list.append(window)
  
  def mainloop(self):
    self.root.mainloop()
  
  def close_all(self):
    self.root.quit()
