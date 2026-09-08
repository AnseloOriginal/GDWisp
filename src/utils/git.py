import git
from src.operations.git.types import GitError
from typing import Callable

def has_repo(path: str):
  """Check if the path provided is a valid git repository"""
  try:
    git.Repo(path)
    return True
  except git.InvalidGitRepositoryError:
    return False

def create_repo(path: str):
  """Creates a new repo"""
  repo = git.Repo.init(path)
  return repo

def run_git_command(
  folder: str,
  command: Callable[[git.Repo],str | None],
  action: str = "do something"
):
  try:
    repo = git.Repo(folder)
    output = command(repo)
    return output
  except git.InvalidGitRepositoryError:
    err: GitError = {
      "msg": f"Repository at {folder} is not valid. Please contact the developers.",
      "title": "Repository invalid."
    }
    return err
  except git.GitCommandError as e:
    err: GitError = {
      "msg": str(e),
      "title": f"Failed to {action}"
    }
    return err