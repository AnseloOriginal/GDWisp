import git
from typing import TypedDict
from src.operations.git.types import GitError

def push(folder: str, remote: str | None):
	try:
		repo = git.Repo(folder)
		branch_name = repo.active_branch.name
		if remote:
			s: str = repo.git.push('--set-upstream', remote, branch_name)
		else:
			s: str = repo.git.push()
		return s
	except git.GitCommandError as e:
		error: GitError = {
			"msg": str(e),
			"title": "Failed to Push"
		}
		return error

def pull(folder: str):
	try:
		repo = git.Repo(folder)
		remote = repo.active_branch.tracking_branch()
		if not remote:
			raise ValueError
		remote = repo.remote(name=remote.remote_name)
		remote.pull()
	except ValueError:
		error: GitError = {
			"msg": "Remote/Server doesn't exists please link remote",
			"title": "Failed to push"
		}
		return error		
	except git.GitCommandError as e:
		error: GitError = {
			"msg": str(e),
			"title": "Failed to Push"
		}
		return error
