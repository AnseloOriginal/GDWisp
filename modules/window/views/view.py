from typing import Literal, TYPE_CHECKING
import customtkinter
from modules.window.views.dashboard_view import view as main_view
from modules.debug.dummy import log_special_message

if TYPE_CHECKING:
  from modules.window.manager import Manager

class GUI_Funtions:
  
  def __init__(self) -> None:
    self.log_special_message = log_special_message

class View_Manager:
  def __init__(self,manager: "Manager") -> None:
    from modules.window.manager import Manager
    self.funcs = GUI_Funtions()
    self.manager = Manager
    
  def create_gui(self,app: customtkinter.CTkToplevel,
  view: Literal["Main"]):
    
    if (view == "Main"):
      main_view(app,self.funcs)









