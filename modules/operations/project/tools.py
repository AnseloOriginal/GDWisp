from modules.operations.git.helpers import safe_get
import modules.operations.project.storage as storage
import modules.operations.git.project as git
from modules.operations.git.tools import get_commit, file_in_commit
from modules.operations.project.storage import get_project_with_data
from typing import cast
from modules.operations.git.diff import Diff
import pathlib
import json

from modules.operations.project.types import ProjectData

def get_project_information(location: str):
	info = {}
	project_data = storage.get_project_with_data(location)
	folder_location = project_data["folder_dir"]
	repo_data = git.repo_data(folder_location)
	merged: dict[str, str] = cast(
		dict[str, str],
		info | repo_data | project_data
	)
	return merged


def diff_from_commit(folder: str, commit1: str, commit2: str | None=None):
	project = get_project_with_data(folder, "folder_dir")
	json_path =  pathlib.Path(project["json_dir"])
	file = json_path.relative_to(folder)
	base_commit = get_commit(folder,commit1)
	raw_base_str = file_in_commit(base_commit,file.as_posix())
	if not raw_base_str:
		return None
	base_project: ProjectData = json.loads(raw_base_str)

	other_commit = get_commit(folder,commit2) if commit2 else safe_get(base_commit.parents,0)
	if other_commit:
		raw_other_str = file_in_commit(other_commit,file.as_posix())
		other_project: ProjectData | None = json.loads(raw_other_str) if raw_other_str else None
	else:
		other_project = None
	return Diff(base_project, other_project)


	
