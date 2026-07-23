import git
from typing import Callable, TypedDict, Union
from src.operations.git.types import GitError


class ProgressUpdate(git.RemoteProgress):
	def __init__(self, on_msg: Callable[[str],None]):
		super().__init__()
		self.on_msg = on_msg

	def update(
		self, 
		op_code: int, 
		cur_count: Union[str, float], 
		max_count: Union[str, float, None] = None, 
		message: str = ""
	) -> None:
		print("NEW MSG:", op_code, cur_count, max_count, message)
		return super().update(op_code, cur_count, max_count, message)

	def new_message_handler(self) -> Callable[[str], None]:
		return self.on_msg

def push(folder: str, remote_name: str | None, progress: ProgressUpdate | None):
	try:
		repo = git.Repo(folder)
		branch_name = repo.active_branch.name
		if remote_name:
			remote = repo.remote(name=remote_name)
			results = remote.push(refspec=branch_name, set_upstream=True, progress=progress)
		else:
			remote_ref = repo.active_branch.tracking_branch()
			if not remote_ref:
				raise ValueError
			remote = repo.remote(name=remote_ref.remote_name)
			results = remote.push(progress=progress)
		if len(results) == 0:
			raise IndexError
		errorList: list[str] = []
		for result in results:
			msg = None
			if result.flags & result.UP_TO_DATE:
				raise IndexError
			if result.flags & result.ERROR:
				msg = f"Error occured in {result.remote_ref_string} due to {result.summary}"
			if result.flags & result.REJECTED:
				msg = f"Commit rejected {result.remote_ref_string} due to {result.summary}"
			if msg:
				errorList.append(msg)
		if len(errorList) > 0:
			fail_count = len(errorList)
			total_count = len(results)
			errorList.insert(0,f"{fail_count} commit(s) failed out of {total_count} pushed")
			error: GitError = {
				"msg": "\n".join(errorList),
				"title": "All commits were not pushed successfully."
			}
			return error
		return True
	except IndexError:
		error: GitError = {
			"msg": "There are no commit(s) to push.",
			"title": "Nothing to push."
		}
		return error
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

def pull(folder: str, progress: ProgressUpdate | None):
	try:
		repo = git.Repo(folder)
		remote = repo.active_branch.tracking_branch()
		if not remote:
			raise ValueError
		remote = repo.remote(name=remote.remote_name)
		result = remote.pull(progress=progress)
		return True
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
