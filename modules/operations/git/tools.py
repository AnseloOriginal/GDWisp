from modules.operations.git.helpers import has_repo
import git


def stage_all_files(location: str):
	repo = git.Repo(location)
	modified_files: list[str] = []
	for item in repo.index.diff(None):
		if (item.a_path):
			modified_files.append(item.a_path)
	repo.index.add(modified_files)
	count = len(modified_files) + len(repo.untracked_files) 
	if repo.untracked_files:
		repo.index.add(repo.untracked_files)
	return {
		"file_count": count,
		"success": True
	}

def commit(location: str, msg: str):
	default_author = git.Actor("Gdevelop User","a@gmail.com")
	repo = git.Repo(location)
	commit = repo.index.commit(msg,author=default_author)
	return {
		"success": True,
		"hexsha": commit.hexsha[0:6]
	}

def commit_list(location: str):
	repo = git.Repo(location)
	commits = repo.iter_commits(all=True, max_count=20)
	return commits