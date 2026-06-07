from modules.operations.git.helpers import has_repo, create_repo
import git
import pathlib
def setup(path: str):
  """Creates and Setup a new repo"""
  if (not has_repo(path)):
    repo = create_repo(path)
  else:
    repo = git.Repo(path)
  create_gitignore(path)

def create_gitignore(path: str):
  """Creates a .gitignore file in project path""" 
  folder = pathlib.Path(path)
  if not folder.is_dir():
      return
  ignore_path = folder / ".gitignore"
  ignore_path.write_text("*.autosave")

