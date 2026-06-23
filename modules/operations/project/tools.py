import modules.operations.project.storage as storage
import modules.operations.git.project as git

def get_project_information(location: str):
	info = {}
	project_data = storage.get_project_by_location(location)
	folder_location = project_data["folder_dir"]
	repo_data = git.repo_data(folder_location)
	merged = info | repo_data
	return merged