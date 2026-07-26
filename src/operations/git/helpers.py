import datetime
from time import perf_counter, timezone

import customtkinter
import git
from git.refs import head
from datetime import datetime, timezone, time

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

class CommitHelper:
  def __init__(self,path: str):
    self.repo = git.Repo(path)

  def get_branch(self, hexsha: str) -> str:
    output: str = self.repo.git.branch("--contains", hexsha)
    for line in output.splitlines():
      if (line.startswith("*")):
        return line.lstrip("* ")
    raise ValueError("Branch not Found for",hexsha)

  def get_refs(self):
    final_refs: list[tuple[str, str]] = []
    try:
      t1 = perf_counter()
      raw_refs: str = self.repo.git.show_ref()
      t2 = perf_counter() - t1
      t3 = perf_counter()
      refs = raw_refs.splitlines()
      for ref in refs:
        hexhsha, name = ref.split(" ")
        final_refs.append((hexhsha, name))
      t4 = perf_counter() - t3
      t5 = t4+t2
      print(f"Using raw_refs got took a total of {t5} (Show ref: {t2}, Parasing: {t4})")
      return final_refs
    except git.GitCommandError:
      return final_refs

  def commits(self,skip: int,max=20):
    print("Skipping:",skip,"with a max:",20)
    commits = self.repo.iter_commits(max_count=max,skip=skip,branches=True)
    return commits

  def no_of_commits(self):
    return int(self.repo.git.rev_list('--count', 'HEAD'))

def safe_get(seq, index, default=None):
    try:
        return seq[index]
    except (TypeError, IndexError, KeyError):
        return default

def current_time():
  return datetime.now(timezone.utc).strftime("%I:%M%p, %d %B %Y").lstrip("0")