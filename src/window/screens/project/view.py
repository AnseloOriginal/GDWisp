import asyncio
from tkinter import COMMAND
import customtkinter
from typing import TYPE_CHECKING, Protocol
from datetime import datetime, timezone, timedelta

from src.core.colors import main_frame
from src.window.screens.project.commitlogic import CommitLogic
from src.window.screens.project.tree import Tree, TreeStructure, generate_tree_data
from src.window.screens.project.timeline import ConsumedCommit, Timeline
from src.window.screens.shared.helpers import AutoHidingScrollFrame, LabeledText, AdvancePadding
from src.window.screens.shared.buttons import multiple_button
from src.window.screens.shared.forced_popup import ForcedPopup
from src.window.screens.project.diff import ProjectViewDiff
from src.window.screens.project.extrainfo import CommitExtraInfo
from src.operations.project.watcher import Projectwatcher
import src.operations.git.tools as git_tools



if TYPE_CHECKING:
  from window.view import GUI_Functions
  from src.operations.git.diff import Diff
  

def view(app: customtkinter.CTkToplevel, funcs: "GUI_Functions", name: str, location: str):
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
    tree = Tree(c1,location,info["folder_dir"])
    tree.grid(row=3,column=1,sticky="ew")
    def on_project_change():
      tree.reset()
      tree.refresh()
    watcher = Projectwatcher(info["folder_dir"],lambda: app.after(0,on_project_change))
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
    
    diff_viewer = ProjectViewDiff(changes_tab,tree.diff,parent=c2)
    diff_viewer.grid(row=0,column=0,sticky="nsew")
    tree.register_click_handler(lambda string: (
      diff_viewer.change_view(string),
      c2.set("Changes View")
    ))
    def on_new_diff(diff):
      print("Recieving")
      diff_viewer.diff = diff
      diff_viewer.refresh()
    tree.register_update_handler(on_new_diff)
    timeline = render_tools(tools_tab,info["folder_dir"])
    diff_viewer.apply_fix(False)
    def on_key_press(evt):
      content = commit_textbox.get("1.0", "end").strip()
      if len(content) > 0 and content != placeholder_text and not tree.no_change:
        commit_butn.configure(state="normal")
      else:
        commit_butn.configure(state="disabled")
    commit_textbox.bind("<KeyRelease>", on_key_press)

    def on_commit():
      def on_success(hexsha):
        commit_textbox.delete("1.0","end")
        tree.reset()
        tree.refresh()
        diff_viewer._render_placeholder()
        commit_butn.configure(state="disabled")
        timeline.check_new_commits()
      msg = commit_textbox.get("1.0", "end").strip()
      commit = CommitLogic(app,msg,info["folder_dir"], on_success)
    commit_butn.configure(command= on_commit)

    def clean_up(event):
      if event.widget == app:
        watcher.stop()
    app.bind("<Destroy>",clean_up)
    def update():
      pass
    return update
  except Exception as e:
    import traceback
    print("CRASHED INSIDE CALLBACK:")
    traceback.print_exc() # Forcibly prints the hidden error trace

def render_tools(parent: customtkinter.CTkFrame, repo_folder: str):
  parent.grid_columnconfigure((0,2), weight=1)
  parent.grid_columnconfigure(1, minsize=2)
  parent.grid_rowconfigure(0, weight=1)
  # divider = customtkinter.CTkFrame(parent,width=2,fg_color="black")
  # divider.grid(column=1,row=0,sticky="ns")

  timeline_section = customtkinter.CTkFrame(parent)
  timeline_section.grid(column=0,row=0,sticky="nsew")
  timeline_section.grid_columnconfigure(1, weight=1)
  timeline_section.grid_rowconfigure(1, weight=1)
  timeline = Timeline(timeline_section,repo_folder)
  timeline.grid(column=1,row=1, sticky="nsew")

  tools = customtkinter.CTkFrame(parent)
  tools.grid(column=2,row=0,sticky="nsew")
  tools.grid_columnconfigure((0,2), minsize=20)
  tools.grid_columnconfigure(1, weight=1)
  # tools.grid_rowconfigure(1, weight=1)

  g1 = AdvancePadding(tools,"Timeline Tools")
  default_text = "—"
  author = LabeledText(g1.padded,"Author",default_text)
  commit_id = LabeledText(g1.padded,"Commit ID",default_text)
  author = LabeledText(g1.padded,"Author",default_text)
  action = LabeledText(g1.padded,"Action",default_text)
  timestamp = LabeledText(g1.padded,"Timestamp",default_text)
  g1.autogrid(author,commit_id,author,action,timestamp,spacing=2)
  f1, b1 = multiple_button(g1.nonpadded,"Extra Info","Diff Commits")
  g1.autogrid(f1,spacing=10)
  g1.grid(column=1,row=1, sticky="nswe")

  g2 = AdvancePadding(tools, "Branch Tools")
  f2, b2 = multiple_button(g2.nonpadded,"Change Branch","Create Branch")
  f3, b3 = multiple_button(g2.nonpadded,"Merge Branch","Delete Branch")
  g2.autogrid(f2,f3,spacing=2)
  g2.grid(column=1,row=2,sticky="nswe",pady=(10,0))

  g3 = AdvancePadding(tools, "Remote Tools")
  f4, b4 = multiple_button(g3.nonpadded,"Add Remote","Sync")
  f5, b5 = multiple_button(g3.nonpadded,"Remove Remote",)
  g2.autogrid(f4,f5,spacing=2)
  g3.grid(column=1,row=3,sticky="nswe",pady=(10,0))

  g4 = AdvancePadding(tools, "Advanced Tools")
  f6, b6 = multiple_button(g4.nonpadded,"Revert","Reset")
  g4.autogrid(f6,spacing=2)
  g4.grid(column=1,row=4,sticky="nswe",pady=(10,0))

  b1[0].configure(state="disabled")
  def on_timeline_click(hexsha: str, commit: ConsumedCommit):
    commit_id.change_text(hexsha[0:6])
    author.change_text(commit.author)
    action.change_text(commit.action)
    tz = timezone(timedelta(seconds=-commit.date_tz))
    time = datetime.fromtimestamp(commit.date,tz)
    timestamp.change_text(time.strftime("%I:%M%p, %d %B %Y").lstrip("0"))
    b1[0].configure(state="active")
    b1[0].configure(command=lambda: CommitExtraInfo(parent,repo_folder,hexsha))
  timeline.ext_funcs = on_timeline_click

  return timeline



