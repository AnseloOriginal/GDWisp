import git
from src.operations.git.types import GitError
from src.operations.git.helpers import run_git_command

def revert(folder: str, hexsha: str):
	return run_git_command(
		folder,
		lambda repo: repo.git.revert(hexsha, no_edit=True),
		f"revert repo to {hexsha}"
	)

def reset(folder: str, hexsha: str):
	return run_git_command(
		folder,
		lambda repo: repo.git.reset('--hard', hexsha),
		f"reset repo to {hexsha}"
	)


def end_revert(folder: str):
	return run_git_command(
		folder,
		lambda repo: repo.git.revert('--abort'),
		f"cleanup revert"
	)