import git
from src.operations.git.types import GitError

def get_remotes(folder: str):
	repo = git.Repo(folder)
	remotes = [remote.name for remote in repo.remotes]
	return remotes

def add_remote(folder: str, name: str, url: str):
	try:
		repo = git.Repo(folder)
		repo.create_remote(name,url)
		return True
	except (git.GitError, OSError) as e:
		error: GitError = {
			"title": "Failed to create remote",
			"msg": str(e)
		}
		return error

def delete_remote(folder: str, name: str):
	try:
		repo = git.Repo(folder)
		remote = repo.remotes[name]
		repo.delete_remote(remote)
		return True
	except KeyError:
		error: GitError = {
			"title": "Failed to delete remote",
			"msg": f"Remote {name} doesn't exist"
		}
		return error
	except (git.GitError, ) as e:
		error: GitError = {
			"title": "Failed to delete remote",
			"msg": str(e)
		}
		return error