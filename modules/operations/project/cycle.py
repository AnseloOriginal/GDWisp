from tkinter import filedialog
from typing import TYPE_CHECKING
import modules.operations.project.storage as storage
import modules.operations.git.project as git
from modules.operations.git.diff import Diff
import json
from modules.operations.project.types import ProjectData

if TYPE_CHECKING:
  from modules.window.manager import Manager

def create_new_project(manager: "Manager"):
  """Prompts the user to create a new project"""
  file_path = filedialog.askopenfilename(
    initialdir="/",
    title="Select Gdevelop Project JSON",
    filetypes=[("Gdevelop JSON", "*.json")]
  )
  if (not file_path): 
    return
  print(file_path)
  try:
    file = open(file_path)
    data = json.loads(file.read())
    name = data["properties"]["name"]
    exist = storage.project_exists(file_path)
    if (not exist):
      folder_path = storage.create_project(name, file_path)
      git.setup(folder_path)
      manager.update_all("Main")  
    else:
      raise ValueError("Project already exists")
  except Exception as e:
    manager.new_window("Error","JSON is corrupt/invaid", "Reason: "+repr(e))

   
def open_project(manager: "Manager", location: str):
  try:
    print("Open Project: ",location)
    project_data = storage.get_project_by_location(location)
    file = open(location)
    project_json = file.read()
    project: ProjectData = json.loads(project_json)
    un_modified_str = git.get_unmodified_file(project_data["folder_dir"],location)
    if un_modified_str:
      un_modified: ProjectData | None = json.loads(un_modified_str)
    else:
      un_modified = None
    diff = Diff(project,un_modified)
  except BaseException:
    pass
