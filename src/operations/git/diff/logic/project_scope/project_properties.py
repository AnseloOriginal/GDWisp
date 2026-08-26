from src.operations.git.diff.logic.per_type import old_new_diff
from src.operations.project.types import ProjectData, ProjectPropertiesData
import src.operations.git.diff.renaming as renaming

def diff_properties(current: ProjectData, old_data: ProjectData | None):
	
	properties = set(ProjectPropertiesData.__annotations__.keys())
	properties.add("gdversion")

	sourcePlusVersion = current["properties"] | {
		"gdversion": f"{getGdevelopVersion(current)}"
	}

	oldPlusVersion = old_data["properties"] | {
		"gdversion": f"{getGdevelopVersion(old_data)}"
	} if old_data else None

	return old_new_diff(properties,sourcePlusVersion,oldPlusVersion,renaming.properties)

def getGdevelopVersion(data: ProjectData | None):
	if not data:
		return data
	return f"{data["gdVersion"].get("major")}.{data["gdVersion"].get("minor")}.{data["gdVersion"].get("build")}"