from src.operations.git.helpers import has_repo
import git
from typing import cast

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
		"hexsha": commit.hexsha
	}

def commit_list(location: str):
	repo = git.Repo(location)
	commits = repo.iter_commits(all=True, max_count=20)
	return commits

def  get_commit(location: str, hexsha: str):
	repo = git.Repo(location)
	return repo.commit(hexsha)


def file_in_commit(commit: git.Commit, file: str):
	try:
		blob = commit.tree / file

		return cast(str, blob.data_stream.read().decode("utf-8"))
	except KeyError: 
		return False
