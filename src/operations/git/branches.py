import git
from typing import TypedDict

class Error(TypedDict):
	title: str
	msg: str

def get_branches(folder: str):
	repo = git.Repo(folder)
	branches = [head.name for head in repo.heads]
	return branches

def create_branch(folder: str, name: str):
	try:
		repo = git.Repo(folder)
		repo.create_head(name)
		return True
	except (git.GitError, OSError) as e:
		error: Error = {
			"title": "Failed to create branch",
			"msg": str(e)
		}
		return error

def checkout_branch(folder: str, name: str):
	try:
		repo = git.Repo(folder)
		branch = repo.heads[name]
		branch.checkout()
		return True
	except git.CheckoutError as e:
		error: Error = {
			"title": "Failed to checkout branch",
			"msg": e.failed_reasons[0]
		}
		return error
	except KeyError as e:
		error: Error = {
			"title": "Failed to checkout branch",
			"msg": f"Branch {name} does not exist"
		}
		return error


def rename_branch(folder: str, branch_name: str, new_name: str):
	try:
		repo = git.Repo(folder)
		branch = repo.heads[branch_name]
		branch.rename(new_name)
		return True
	except git.GitError as e:
		error: Error = {
			"title": "Failed to rename branch",
			"msg": str(e)
		}
		return error
	except KeyError as e:
		error: Error = {
			"title": "Failed to rename branch",
			"msg": f"Branch {branch_name} does not exist"
		}
		return error

def delete_branch(folder: str, name: str):
	try:
		repo = git.Repo(folder)
		branch = repo.heads[name]
		repo.delete_head(branch)
		return True
	except git.GitError as e:
		error: Error = {
			"title": "Failed to delete branch",
			"msg": str(e)
		}
		return error
	except KeyError as e:
		error: Error = {
			"title": "Failed to delete branch",
			"msg": f"Branch {name} does not exist"
		}
		return error