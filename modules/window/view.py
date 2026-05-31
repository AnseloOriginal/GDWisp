import customtkinter
from modules.media.image import ICON

def set_main_view(app: customtkinter.CTkToplevel):
  testProjects = [
    ("Cool Game","Yesterday"),
    ("Stupid Game","Last Week")
  ]
  customtkinter.set_appearance_mode("dark")
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
  add_project_butn = create_icon_butn(c1,"Add Project","add",text_colors,button_colors,1,4,hover_colors=hover_colors)
  diff_project_butn = create_icon_butn(c1,"Diff Tool","diff",text_colors,button_colors,1,5,hover_colors=hover_colors)
  settings_project_butn = create_icon_butn(c1,"Settings","settings",text_colors,button_colors,1,6,hover_colors=hover_colors)
  help_project_butn = create_icon_butn(c1,"Help","help",text_colors,button_colors,1,7,hover_colors=hover_colors)
  project_title = customtkinter.CTkLabel(c2, text="Projects", text_color=("#000000","#FFFFFF"), font=(None, 24, "bold"))
  project_title.grid(row=2,column=1)
  row = 3
  for project in testProjects:
    project_butn = create_project_butn(c2, project[0],project[1],text_colors,button_colors,small_text_colors,1,row,hover_colors=hover_colors)
    row = row + 1

def create_icon_butn(
    parent: customtkinter.CTkFrame, text: str, 
    icon: str, text_color: tuple,
    butn_color: tuple,
    col: int, row: int,
    width: int = 200,
    height: int = 40,
    font_size: int=20,
    pady=5,
    padx=0,
    hover_colors=(None, None)
  ): 
  image = customtkinter.CTkImage(ICON[icon])
  butn = customtkinter.CTkButton(
    parent, 
    text=text,
    text_color = text_color,
    fg_color= butn_color,
    image= image,
    compound="left",
    width=width,
    height=height,
    font=(None,font_size),
    hover_color=hover_colors
  )
  butn.grid(row=row, column=col, pady=pady)
  return butn

def create_project_butn(
  parent: customtkinter.CTkFrame,
  main_text: str, small_text: str,
  main_text_color: tuple, butn_color: tuple, small_text_color: tuple,
  col: int, row: int,
  main_font_size=20, small_font_size=10,
  width: int = 200, height: int = 500,
  pady=5, padx=0,
  hover_colors=(None, None),
  sticky="nsew"
): 
  fake_butn = customtkinter.CTkFrame(parent, fg_color=butn_color, width=width, height=height)
  fake_butn.grid(column=col, row=row, padx=padx, pady=pady, sticky=sticky)
  fake_butn.grid_columnconfigure(0,minsize=10)
  fake_butn.grid_columnconfigure(3,minsize=10)
  
  fake_butn.grid_columnconfigure(2,weight=1)
  main_label = customtkinter.CTkLabel(fake_butn, text=main_text, font=(None,main_font_size), text_color=main_text_color)
  main_label.grid(column=1,row=1)
  small_label = customtkinter.CTkLabel(fake_butn, text=small_text, font=(None,small_font_size), text_color=small_text_color)
  small_label.grid(column=2,row=1, sticky='se')
  def on_hover(event):
    fake_butn.configure(fg_color=hover_colors)

  def on_unhover(event):
    fake_butn.configure(fg_color=butn_color)
  
  def on_click(event):
    fake_butn.configure(fg_color=butn_color)

  fake_butn.bind("<Enter>", on_hover)
  fake_butn.bind("<Leave>",on_unhover)
  fake_butn.bind("<Button-1>",on_click)
  return fake_butn
  

