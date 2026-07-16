from src.operations.git.helpers import has_repo, create_repo
import git
import pathlib
from typing import cast

def setup(path: str):
  """Creates and Setup a new repo"""
  if (not has_repo(path)):
    repo = create_repo(path)
  else:
    repo = git.Repo(path)
  create_gitignore(path)
  return repo

def create_gitignore(path: str):
  """Creates a .gitignore file in project path""" 
  folder = pathlib.Path(path)
  if not folder.is_dir():
      return
  ignore_path = folder / ".gitignore"
  ignore_path.write_text("*.autosave")


def get_unmodified_file(path_to_repo: str, path_to_file: str):
  """Gets the unmodified file from the repo. Only utf-8 srings are supported"""
  path =  pathlib.Path(path_to_file)
  relative_path = path.relative_to(path_to_repo)

  if (not has_repo(path_to_repo)):
    print("No Repo")
    return None
  
  try:
    repo = git.Repo(path_to_repo)
  
    if relative_path.as_posix() in repo.untracked_files:
      print("Not Tracked")      
      return None
    blob = repo.head.commit.tree / relative_path
    data: str = cast(str,blob.data_stream.read().decode('utf-8'))
    return data
  except (UnicodeDecodeError, ValueError, KeyError):
    return None

  

def repo_data(path_to_repo: str):
  data: dict[str, str] = {}
  if (not has_repo(path_to_repo)):
    return data
  repo = git.Repo(path_to_repo)
  data["branch"] = repo.active_branch.name
  return data