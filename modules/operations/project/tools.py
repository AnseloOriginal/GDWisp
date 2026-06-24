import modules.operations.project.storage as storage
import modules.operations.git.project as git
from typing import cast

def get_project_information(location: str):
	info = {}
	project_data = storage.get_project_by_location(location)
	folder_location = project_data["folder_dir"]
	repo_data = git.repo_data(folder_location)
	merged: dict[str, str] = cast(
		dict[str, str],
		info | repo_data | project_data
	)
	return merged