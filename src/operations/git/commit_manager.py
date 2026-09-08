import git
from time import perf_counter

class CommitManager:
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
    if self.repo.head.is_valid():
      print("Skipping:",skip,"with a max:",20)
      commits = self.repo.iter_commits(max_count=max,skip=skip,branches=True)
      return commits
    else:
      return []

  def no_of_commits(self):
    try:
      return int(self.repo.git.rev_list('--count', 'HEAD'))
    except git.GitCommandError:
      return 0