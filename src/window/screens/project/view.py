import asyncio
from tkinter import COMMAND
import customtkinter
from typing import TYPE_CHECKING, Literal
from datetime import datetime, timezone, timedelta

from src.core.colors import main_frame
from src.window.screens.project.commitlogic import CommitLogic
from src.window.screens.project.tree import Tree, TreeStructure, generate_tree_data
from src.window.screens.project.timeline import BranchLine, ConsumedCommit, Timeline
from src.window.screens.shared.helpers import AutoHidingScrollFrame, LabeledText, AdvancePadding
from src.window.screens.shared.buttons import multiple_button
from src.window.screens.shared.forced_popup import ForcedPopup
from src.window.screens.project.diff import ProjectViewDiff
from src.window.screens.project.extrainfo import CommitExtraInfo
from src.window.screens.project.branch_tool import BranchTool
from src.window.screens.project.remote_tool import RemoteTool
from src.window.screens.project.stash_tool import StashTool
from src.window.screens.project.branch_tool import modes as BranchToolModes
from src.window.screens.project.sync_tool import SyncTool
from src.window.screens.project.timeline_action import TimelineAction, SelectedCommit
from src.operations.project.watcher import Projectwatcher
import src.operations.git.tools as git_tools
from src.operations.git.watcher import GitWatcher, EventPayload

if TYPE_CHECKING:
  from window.view import GUI_Functions
  from src.operations.git.diff.main import Diff
  

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
    tools_tab = c2.add("Timeline & Tools")
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

    sync_butn = quick_create(c1,"Sync")
    sync_butn.grid(row=11, column=1, sticky="ew")
    def update_sync_butn(is_tracked: bool | str):
      text = "Sync" if is_tracked else "Link to Remote"
      sync_butn.configure(
        text = text,
        command=lambda: SyncTool(c1,info["folder_dir"],"link")
      )
    update_sync_butn(info["is_tracked"])
    
    diff_viewer = ProjectViewDiff(changes_tab,tree.diff,parent=c2)
    diff_viewer.grid(row=0,column=0,sticky="nsew")
    tree.register_click_handler(lambda string: (
      diff_viewer.change_view(string),
      c2.set("Changes View")
    ))
    def on_new_diff(diff):
      diff_viewer.diff = diff
      diff_viewer.refresh()
    tree.register_update_handler(on_new_diff)
    timeline = render_tools(tools_tab,info["folder_dir"])
    diff_viewer.apply_fix(False)

    def apply_c2_fix():
      tabname = c2.get()
      if tabname != "Changes View":
        diff_viewer.apply_fix(True)
      elif diff_viewer.current_view == "placeholder":
        diff_viewer.apply_fix(False)
    c2.configure(command=apply_c2_fix)

    def on_key_press(evt):
      content = commit_textbox.get("1.0", "end").strip()
      if len(content) > 0 and content != placeholder_text and not tree.no_change:
        commit_butn.configure(state="normal")
      else:
        commit_butn.configure(state="disabled")
    commit_textbox.bind("<KeyRelease>", on_key_press)

    def on_git_change(action: Literal["commit", "branch"], payload: EventPayload | None):
      if action == "commit":
        timeline.check_new_commits()
      if not payload:
        return
      if "name" in payload:
         current_branch.configure(
          text="Current Branch: "+payload["name"]
        )
      if "is_tracked" in payload:
        update_sync_butn(payload["is_tracked"])
    def run_on_git_change(
      action: Literal["commit", "branch"], 
      payload: EventPayload | None
    ):
      app.after(0, on_git_change, action, payload)
    git_watcher = GitWatcher(info["folder_dir"],run_on_git_change)

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
  f3, b3 = multiple_button(g2.nonpadded,"Rename Branch","Delete Branch")
  g2.autogrid(f2,f3,spacing=2)
  g2.grid(column=1,row=2,sticky="nswe",pady=(10,0))

  g3 = AdvancePadding(tools, "Remote Tools")
  f4, b4 = multiple_button(g3.nonpadded,"Add Remote","Remove Remote")
  f5, b5 = multiple_button(g3.nonpadded,"Push","Pull")
  g2.autogrid(f4,f5,spacing=2)
  g3.grid(column=1,row=3,sticky="nswe",pady=(10,0))

  g4 = AdvancePadding(tools, "Advanced Tools")
  f6, b6 = multiple_button(g4.nonpadded,"Revert","Reset")
  f7, b7 = multiple_button(g4.nonpadded,"Merge")
  f8, b8 = multiple_button(g4.nonpadded,"Restore")
  g4.autogrid(f6, f7, f8, spacing=2)
  g4.grid(column=1,row=4,sticky="nswe",pady=(10,0))

  selected: SelectedCommit = {
    "summary": None,
    "hexsha": None
  }

  b1[0].configure(state="disabled")
  def on_timeline_update(hexsha: str, commit_or_refresh: ConsumedCommit | bool):
    if not isinstance(commit_or_refresh,bool):
      commit = commit_or_refresh
      selected["hexsha"] = hexsha
      selected["summary"] = commit.summary
      commit_id.change_text(hexsha[0:6])
      author.change_text(commit.author)
      action.change_text(commit.action)
      tz = timezone(timedelta(seconds=-commit.date_tz))
      time = datetime.fromtimestamp(commit.date,tz)
      timestamp.change_text(time.strftime("%I:%M%p, %d %B %Y").lstrip("0"))
      b1[0].configure(state="active")
      b1[0].configure(command=lambda: CommitExtraInfo(parent,repo_folder,hexsha))
    elif commit_or_refresh:
      selected["hexsha"] = None
      selected["summary"] = None
      commit_id.change_text("-")
      author.change_text("-")
      action.change_text("-")
      timestamp.change_text("-")

  timeline.ext_funcs = on_timeline_update
  def configure_butn_tool(
    button: customtkinter.CTkButton, 
    mode: BranchToolModes,
    action_type: Literal["Remote", "Branch"] = "Branch"
  ):
    if action_type == "Branch":
      button.configure(command=lambda: BranchTool(parent,mode,repo_folder))
    else:
      button.configure(command=lambda: RemoteTool(parent,mode,repo_folder))

  configure_butn_tool(b2[0],"change")
  configure_butn_tool(b2[1],"create")
  configure_butn_tool(b3[0],"rename")
  configure_butn_tool(b3[1],"delete")
  configure_butn_tool(b7[0],"merge")
  configure_butn_tool(b4[0],"create","Remote")
  configure_butn_tool(b4[1],"delete","Remote")
  b5[0].configure(command=lambda: SyncTool(parent,repo_folder,"push"))
  b5[1].configure(command=lambda: SyncTool(parent,repo_folder,"pull"))
  b6[0].configure(command=lambda: TimelineAction(repo_folder,parent,"revert",selected))
  b6[1].configure(command=lambda: TimelineAction(repo_folder,parent,"reset",selected,
    timeline.refresh))
  b8[0].configure(command=lambda: StashTool(parent,"restore",repo_folder))
  return timeline



