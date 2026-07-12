import json
from modules.operations.git.diff import Diff
import modules.operations.git.project as git
from modules.operations.project.types import ProjectData


def project_diff(file_dir: str, folder_dir: str):
	file = open(file_dir)
	project_json = file.read()
	project: ProjectData = json.loads(project_json)
	un_modified_str = git.get_unmodified_file(folder_dir,file_dir)
	if un_modified_str:
		un_modified: ProjectData | None = json.loads(un_modified_str)
	else:
		un_modified = None
	return Diff(project,un_modified)