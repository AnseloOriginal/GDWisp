import customtkinter
from src.window.screens.shared.buttons import create_icon_butn, create_project_butn
from typing import TYPE_CHECKING, Callable
from src.core.colors import main_frame, theme_colors
from src.utils.settings import is_configured
from src.window.screens.dashboard.welcome_menu import  WelcomeMenu
if TYPE_CHECKING:
  from src.window.view import GUI_Functions

def fill_project_area(c2: customtkinter.CTkFrame, data: list[tuple[str, str, str]], onclick: Callable[[str], None]):
  entity_list: list[customtkinter.CTkLabel | customtkinter.CTkFrame] = []
  start_row = 3
  if len(data) == 0:
    no_project_title = customtkinter.CTkLabel(
                          c2, 
                          text="No Projects yet. Add one to get started.",
                          font=(None, 18)
                        )

    no_project_title.grid(row=3,column=1)
    entity_list.append(no_project_title)
  text_color = theme_colors["butn_text_color"]
  butn_color = theme_colors["butn_color"]
  small_text_color = theme_colors["small_text_color"]
  hover_color = theme_colors["hover_color"]

  for project in data:
    click = lambda target=project[2]: onclick(target)
    project_butn = create_project_butn(c2, project[0],project[1],
    text_color,butn_color,small_text_color,1,start_row,
    hover_color=hover_color, onclick=click)
    start_row = start_row + 1
    entity_list.append(project_butn)
  return entity_list


def view(app: customtkinter.CTkToplevel, funcs: "GUI_Functions"):
  if not is_configured():
    WelcomeMenu(app)
    
  projects = funcs.get_projects_by_date()
  
  customtkinter.set_appearance_mode("light")
  app.title("Gdevelop Forge")
  app.grid_columnconfigure(0, weight=1)
  app.grid_columnconfigure(1, weight=1, minsize=300)
  app.grid_columnconfigure(2, weight=1, minsize=300)
  app.grid_columnconfigure(3, weight=1)
  app.grid_rowconfigure(0, minsize=40, weight=0)
  app.grid_rowconfigure(1, weight=1)
  

  c1 = customtkinter.CTkFrame(app, width=300)
  c1.configure(
    fg_color=main_frame["color"],
    border_color=main_frame["border_color"],
    border_width=main_frame["border_width"]
  )
  c1.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
  c1.grid_columnconfigure(0,weight=1)
  c1.grid_columnconfigure(2,weight=1)
  c1.grid_rowconfigure(0,minsize=10)

  c2 = customtkinter.CTkFrame(app, width=300)
  c2.configure(
    fg_color=main_frame["color"],
    border_color=main_frame["border_color"],
    border_width=main_frame["border_width"]
  )
  c2.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")
  c2.grid_columnconfigure(0,minsize=50)
  c2.grid_columnconfigure(1,minsize=200,weight=1)
  c2.grid_columnconfigure(2,minsize=50)
  c2.grid_rowconfigure(0,minsize=10)
  main_title = customtkinter.CTkLabel(c1, text="Gdevelop SVN", font=(None, 24, "bold"))
  main_title.grid(row=2,column=1)

  add_project_butn = create_icon_butn(c1,"Add Project","add",None,None,1,4, command=funcs.add_new_project)
  diff_project_butn = create_icon_butn(c1,"Diff Tool","diff",None,None,1,5)
  settings_project_butn = create_icon_butn(c1,"Settings","settings",None,None,1,6)
  help_project_butn = create_icon_butn(c1,"Help","help",None,None,1,7)
  project_title = customtkinter.CTkLabel(c2, text="Projects", font=(None, 24, "bold"))
  project_title.grid(row=2,column=1)
  c2_list = fill_project_area(c2,projects,funcs.open_project)
  
  def update():
    projects = funcs.get_projects_by_date()
    for entity in c2_list:
      entity.destroy()
      c2_list.remove(entity)
    for entity in fill_project_area(c2,projects,funcs.open_project):
      c2_list.append(entity)

    
  return update
  
