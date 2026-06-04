import customtkinter
from modules.window.views.helpers import create_icon_butn, create_project_butn
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from modules.window.views.view import GUI_Functions

def view(app: customtkinter.CTkToplevel, funcs: "GUI_Functions"):
  projects = funcs.get_projects_by_date()
  customtkinter.set_appearance_mode("light")
  app.title("Gdevelop SVN")
  app.configure(fg_color=["#FFFFFF","#18181B"])
  app.grid_columnconfigure(0, weight=1)
  app.grid_columnconfigure(1, weight=1, minsize=300)
  app.grid_columnconfigure(2, weight=1, minsize=300)
  app.grid_columnconfigure(3, weight=1)
  app.grid_rowconfigure(0, minsize=40, weight=0)
  app.grid_rowconfigure(1, weight=1)
  

  c1 = customtkinter.CTkFrame(app, width=300)
  c1.configure(fg_color=["#FAFAFA","#313236"], border_color=["#586CA3","#575961"], 
               border_width=1)
  c1.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
  c1.grid_columnconfigure(0,weight=1)
  c1.grid_columnconfigure(2,weight=1)
  c1.grid_rowconfigure(0,minsize=10)

  c2 = customtkinter.CTkFrame(app, width=300)
  c2.configure(fg_color=["#FAFAFA","#313236"], border_color=["#586CA3","#575961"], 
               border_width=1)
  c2.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")
  c2.grid_columnconfigure(0,minsize=50)
  c2.grid_columnconfigure(1,minsize=200,weight=1)
  c2.grid_columnconfigure(2,minsize=50)
  c2.grid_rowconfigure(0,minsize=10)
  main_title = customtkinter.CTkLabel(c1, text="Gdevelop SVN", text_color=("#000000","#FFFFFF"), font=(None, 24, "bold"))
  main_title.grid(row=2,column=1)
  button_colors = ("#D9D4FF", "#D9D4FF")
  small_text_colors = ("#103C7D", "#103C7D")
  text_colors = ("#000000", "#000000")
  hover_colors = ("#BDB7FA", "#BDB7FA")
  add_project_butn = create_icon_butn(c1,"Add Project","add",text_colors,button_colors,1,4,hover_colors=hover_colors, command=funcs.add_new_project)
  diff_project_butn = create_icon_butn(c1,"Diff Tool","diff",text_colors,button_colors,1,5,hover_colors=hover_colors)
  settings_project_butn = create_icon_butn(c1,"Settings","settings",text_colors,button_colors,1,6,hover_colors=hover_colors)
  help_project_butn = create_icon_butn(c1,"Help","help",text_colors,button_colors,1,7,hover_colors=hover_colors)
  project_title = customtkinter.CTkLabel(c2, text="Projects", text_color=("#000000","#FFFFFF"), font=(None, 24, "bold"))
  project_title.grid(row=2,column=1)
  row = 3
  if len(projects) == 0:
    no_project_title = customtkinter.CTkLabel(c2, text="No Projects yet. Add one to get started.", 
                           text_color=("#000000","#FFFFFF"), font=(None, 18))
    no_project_title.grid(row=3,column=1)
    
  for project in projects:
    project_butn = create_project_butn(c2, project[0],project[1],text_colors,button_colors,small_text_colors,1,row,hover_colors=hover_colors)
    row = row + 1
