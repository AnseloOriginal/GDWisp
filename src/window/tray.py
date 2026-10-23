import pystray
from collections.abc import Callable

class Tray:
  """App Tray"""
  click_fucns = []
  new_window_fucns: list[Callable] = []
  quit_fucns: list[Callable] = []

  def __init__(self,image):
    self.menu = pystray.Menu(
      pystray.MenuItem("New Window",self.on_new_window),
      pystray.MenuItem("Quit",self.quit)
    )
    self.icon = pystray.Icon("GDWisp",image, "GDWisp",self.menu)
    self.icon.run_detached()
  
  def on_new_window(self):
    for func in self.new_window_fucns:
      func()
    
  
  def quit(self):
    self.icon.stop()
    for func in self.quit_fucns:
      func()
    

  def register_on_new(self,func: Callable):
    self.new_window_fucns.append(func)

  def register_on_quit(self,func: Callable):
    self.quit_fucns.append(func)
  

  