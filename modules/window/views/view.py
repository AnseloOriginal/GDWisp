from typing import Literal, TYPE_CHECKING
import customtkinter
from modules.window.views.dashboard_view import view as main_view
from modules.window.views.error_view import view as error_view
from modules.debug.dummy import log_special_message
from modules.operations.project.cycle import create_new_project
from modules.window.types import VIEW_TYPE
import modules.operations.project.storage as storage

if TYPE_CHECKING:
  from modules.window.manager import Manager

class GUI_Functions:
  
  def __init__(self,manager: "Manager") -> None:
    self.manager = manager
    self.log_special_message = log_special_message
    self.add_new_project = lambda: create_new_project(manager)
    self.get_projects_names = storage.get_projects_by_date
    self.get_projects_by_date = storage.get_projects_by_date


class View_Manager:
  def __init__(self,manager: "Manager", *extras) -> None:
    from modules.window.manager import Manager
    self.funcs = GUI_Functions(manager)
    self.manager = manager
    
  def create_gui(self,app: customtkinter.CTkToplevel, view: VIEW_TYPE,*extras):
    if (view == "Main"):
      main_view(app,self.funcs)
    elif (view == "Error"):
      error_view(app,self.funcs,extras[0],extras[1])
      










