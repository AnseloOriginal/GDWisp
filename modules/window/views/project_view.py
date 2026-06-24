import asyncio
from tkinter import COMMAND
import customtkinter
from typing import TYPE_CHECKING, Protocol

import git
from modules.config.colors import main_frame
from modules.window.views.tree import Tree, TreeStructure
from modules.window.views.helpers import ForcedPopup
from modules.window.views.project_view_diff import ProjectViewDiff
import modules.operations.git.tools as git_tools 

if TYPE_CHECKING:
  from modules.window.views.view import GUI_Functions
  from modules.operations.git.diff import Diff

def generate_tree_data(diff: "Diff"): 
  data: TreeStructure = {}
  if (diff.propertiesDiff != None):
    if (data.get("Project", None) == None):
      data["Project"] = {}
    data["Project"]["Properties"] = "properties"
  return data

def view(app: customtkinter.CTkToplevel, funcs: "GUI_Functions", name: str, location: str, diff: "Diff"):
  try:
    info = funcs.get_project_information(location)
    app.title("Gdevelop Project: "+name)
    app.geometry("900x600")
    app.minsize(1000,600)
    app.grid_columnconfigure((0,4), minsize=50)
    app.grid_columnconfigure(1, weight=1,)
    app.grid_columnconfigure(2, minsize=25)
    app.grid_columnconfigure(3, weight=5)
    app.grid_rowconfigure((0,2), minsize=40)
    app.grid_rowconfigure(1, weight=1)

    c1 = customtkinter.CTkFrame(
      app, 
      width=75,
      fg_color=main_frame["color"],
      border_color=main_frame["border_color"],
      border_width=main_frame["border_width"]
    )
    c1.grid_rowconfigure((0,2,4,6,8,10,12), minsize=10)
    c1.grid_columnconfigure((0,2), minsize=20)
    c1.grid_rowconfigure(3, weight=1, minsize=200)
    c1.grid_rowconfigure(7, weight=1, minsize=100)
    c1.grid_columnconfigure(1, weight=1, minsize=50)
    c2 = customtkinter.CTkTabview(
      app, 
      fg_color=main_frame["color"],
      border_color=main_frame["border_color"],
      border_width=main_frame["border_width"],

    )
    c2.grid_rowconfigure(0, minsize=0, weight=0)
    # c2._outer_button_overhang = 0
    # app.after(500, lambda: c2._segmented_button.grid_remove())
    c1.grid(row=1, column=1, sticky="nsew")#, pady=(20,0))
    c2.grid(row=1, column=3, sticky="nsew")
    changes_tab = c2.add("Changes View")
    changes_tab.grid_rowconfigure(0, weight=1)
    changes_tab.grid_columnconfigure(0, weight=1)
    tools_tab = c2.add("Tools")
    roadmap_tab = c2.add("Roadmap Tools")
    app.focus()
    app.after(10, lambda: app.state('zoomed'))

    for button in c2._segmented_button._buttons_dict.values():
      button.configure(width=100, height=40) # Set your size in pixels

    changes_text = customtkinter.CTkLabel(c1, text="Changes",font=(None, 18, "bold"),anchor="w")
    changes_text.grid(row=1, column=1, sticky="ew")
    tree_data = generate_tree_data(diff)
    tree = Tree(c1,tree_data,False)
    tree.grid(row=3,column=1,sticky="ew")
    current_branch = customtkinter.CTkLabel(c1, text="Current Branch: "+info.get("branch","Unknown"),
      font=(None, 18, "bold"),anchor="w")
    current_branch.grid(row=5, column=1, sticky="ew")
    commit_textbox = customtkinter.CTkTextbox(c1,width=100, height=200)
    commit_textbox.grid(row=7, column=1, sticky="ew")
    placeholder_text = "Enter details of your changes."
    commit_textbox.insert("0.0", placeholder_text)
    button_height = 30


    quick_create = lambda master,text: customtkinter.CTkButton(master, height=button_height, text=text)
    commit_butn = quick_create(c1,"Commit")
    commit_butn.grid(column=1,row=9,sticky="ew")
    commit_butn.configure(state="disabled")

    two_butn_space = customtkinter.CTkFrame(c1, width=button_height)
    two_butn_space.grid(row=11, column=1, sticky="ew")
    two_butn_space.grid_columnconfigure(1,minsize=20)
    two_butn_space.grid_columnconfigure(0,weight=1)
    two_butn_space.grid_columnconfigure(2,weight=1)
    push_butn = quick_create(two_butn_space,"Push")
    pull_butn = quick_create(two_butn_space,"Pull")
    push_butn.grid(column=0,row=0,sticky="ew")
    pull_butn.grid(column=2,row=0,sticky="ew")
    
    diff_viewer = ProjectViewDiff(changes_tab,diff,parent=c2)
    diff_viewer.grid(row=0,column=0,sticky="nsew")
    tree.register_handler(lambda string: (
      diff_viewer.change_view(string),
      c2.set("Changes View")
    ))

    def on_key_press(evt):
      content = commit_textbox.get("1.0", "end").strip()
      if len(content) > 0 and content != placeholder_text:
        commit_butn.configure(state="normal")
      else:
        commit_butn.configure(state="disabled")
    commit_textbox.bind("<KeyRelease>", on_key_press)

    async def on_commit():
      popup = ForcedPopup(app)
      stage = "starting"
      try:
        msg = commit_textbox.get("1.0", "end").strip()
        popup.title("Starting Commit")
        popup.add_text("Starting commit. Please wait...",False)
        folder: str = info["folder_dir"]
        stage = "staging"
        result1 = await asyncio.to_thread(git_tools.stage_all_files, folder)        
        popup.add_text(f"Staged {result1['file_count']} file(s) for commit")
        stage = "committing"
        if (result1['file_count'] == 0):
          raise ValueError("cannot commit with no changes")
        result2 = await asyncio.to_thread(git_tools.commit, folder, msg)
        popup.add_text(f"Commit successful ({result2['hexsha']})",True,"success")
        popup.show_close(True)
      except Exception as e:
        popup.add_text(f"Commit failed during {stage} stage",True,"error")
        popup.add_text(f"Reason for failure is {str(e)}",True,"error")
        popup.show_close(True)
      
    commit_butn.configure(command=lambda: asyncio.run(on_commit()))
    def update():
      pass
    return update
  except Exception as e:
    import traceback
    print("CRASHED INSIDE CALLBACK:")
    traceback.print_exc() # Forcibly prints the hidden error trace