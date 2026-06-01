import customtkinter
from modules.window.views.view import View_Manager

class Manager:
  """Manages windows"""
  app_window_list: list[customtkinter.CTkToplevel] = []
  
  def __init__(self) -> None:
    root = customtkinter.CTk()
    root.withdraw()
    self.root = root
    self.view = View_Manager(self)

  def new_window(self):
    window = customtkinter.CTkToplevel(self.root)
    window.geometry("800x600")
    self.view.create_gui(window,"Main")
    self.app_window_list.append(window)
  
  def mainloop(self):
    self.root.mainloop()
  
  def close_all(self):
    self.root.quit()
