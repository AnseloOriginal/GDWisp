from platformdirs import user_data_path
import json
import pathlib
from typing import TypedDict
from datetime import datetime, timezone
from math import floor

class project_data(TypedDict):
  name: str
  json_dir: str
  folder_dir: str
  last_accessed: str

folder_path = user_data_path(appname="GdevelopSVN",ensure_exists=True, roaming=True)
storage_path = folder_path / "projects.json"

project_list: list[project_data] = []

def related_date_str(later: datetime):
  """Get string relating current time with given time e.g 5 hours"""
  current = datetime.now(timezone.utc)
  diff = current - later 
  if diff.seconds < 30:
    return "Now"
  elif diff.days < 1:
    is_hour = True if diff.seconds >= 3600 else False
    hour = floor(diff.seconds / 3600)
    minutes = floor(diff.seconds / 60)
    time = hour if is_hour else minutes
    time_str = "hour" if is_hour else "minutes"
    plural_str = "" if time == 1 else "s"
    return "{} {}{} ago".format(str(time),time_str,plural_str)
  elif diff.days == 1:
    return "1 day ago"
  else:
    return str(diff.days) + " days ago"

def load_app_list():
  """Loads the project list from storage"""
  try: 
    data = open(storage_path,"r")
    temp: list[project_data] = json.loads(data.read())
    project_list.clear()
    for project in temp:
      project_list.append(project)
    print("Found "+str(len(temp))+" projects.")
  except:
    print("No User Project Exists")

def get_projects_name():
  """Gets a list of project names"""
  names: list[str] = []
  for project in project_list:
    names.append(project["name"])
  return names

def get_projects_by_date():
  """Get a project list sorted by when there were last accessed"""
  sorted_projects = sorted(
      project_list, 
      key=lambda x: datetime.fromisoformat(x["last_accessed"]), 
      reverse=True
  )
  names: list[tuple[str, str]] = []
  for project in sorted_projects:
      last_accessed = datetime.fromisoformat(project["last_accessed"])
      names.append((project["name"], related_date_str(last_accessed)))
  return names

def project_exists(filepath):
  """Returns true if a project already exist with given json path"""
  exists = False
  for project in project_list:
    if project["json_dir"] == filepath:
      exists = True
  return exists
  

def create_project(name: str, file_path: str):
  """Adds a new project and write to disk"""
  folder_path = str(pathlib.Path(file_path).parent)
  current_time = datetime.now(timezone.utc).isoformat()

  project_dict: project_data = {
    "name": name,
    "json_dir": file_path,
    "folder_dir": folder_path,
    "last_accessed": current_time
  }
  project_list.append(project_dict)
  write_to_disk()

def write_to_disk():
  """Write the project list to its json file"""
  data = json.dumps(project_list)
  storage_path.write_text(data)