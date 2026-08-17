from tkinter import filedialog
from typing import TYPE_CHECKING
from src.operations.project.diff_related import project_diff
import src.operations.project.storage as storage
import src.operations.git.project as git
import json
from src.operations.project.types import ProjectData

if TYPE_CHECKING:
  from src.window.manager import Manager

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
    print("Open Project: ",location)
    project_data = storage.get_project_with_data(location)
    manager.new_window("Project",project_data["name"],location)
    storage.project_modified(project_data["name"])
    manager.update_all("Main")
  