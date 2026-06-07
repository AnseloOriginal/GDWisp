import git

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

