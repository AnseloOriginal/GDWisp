import git
from typing import TypedDict
from src.operations.git.helpers import current_time
from src.operations.git.types import GitError
from src.core.constants import app_name

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
		error: GitError = {
			"title": "Failed to create branch",
			"msg": str(e)
		}
		return error

def checkout_branch(folder: str, name: str):
	try:
		repo = git.Repo(folder)
		is_dirty = repo.is_dirty(untracked_files=True)
		if is_dirty:
			repo.git.stash("save","-u", 
				f"{app_name}-autostash/{repo.active_branch.name} on {current_time()}"
			)
		branch = repo.heads[name]
		branch.checkout()
		return True
	except git.GitCommandError as e:
		error: GitError = {
			"title": "Failed to checkout branch",
			"msg": str(e)
		}
		return error
	except git.CheckoutError as e:
		error: GitError = {
			"title": "Failed to checkout branch",
			"msg": e.failed_reasons[0]
		}
		return error
	except KeyError as e:
		error: GitError = {
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
		error: GitError = {
			"title": "Failed to rename branch",
			"msg": str(e)
		}
		return error
	except KeyError as e:
		error: GitError = {
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
		error: GitError = {
			"title": "Failed to delete branch",
			"msg": str(e)
		}
		return error
	except KeyError as e:
		error: GitError = {
			"title": "Failed to delete branch",
			"msg": f"Branch {name} does not exist"
		}
		return error

def is_dirty(folder: str):
	try:
		repo = git.Repo(folder)
		return repo.is_dirty(untracked_files=True)
	except git.GitError:
		return False

def extract_stash_info(stash_str: str):
	stash: dict[str, str] = {}
	lines = stash_str.splitlines()
	for line in lines:
		if not app_name in line:
			continue
		branch_index = line.find(f"{app_name}-autostash/")+len(app_name)+11
		branch_name = line[branch_index:]
		stash_index = line.find(":")
		stash_name = line[:stash_index]
		stash[branch_name] = stash_name
	return stash
