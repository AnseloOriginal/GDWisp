
from src.operations.git.helpers import run_git_command

def pretify(text: str):
	start = text.find("On")
	start = text.find("WIP") if start == -1 else start
	return (text[:start-2], text[start:])

def get_all_stash(folder: str)-> list[tuple[str, str]]:
	results = run_git_command(
		folder,
		lambda repo: repo.git.stash("list"),
		"getting stashes"
	)
	if type(results) is not str:
		return []
	raw_list = results.splitlines()
	pretty_list = [pretify(stash) for stash in raw_list]
	return pretty_list


def pop_stash(folder: str, stash_id: str):
	results = run_git_command(
		folder,
		lambda repo: repo.git.stash("pop",stash_id),
		f"restoring/popping {stash_id}"
	)
	return results

	