from src.operations.git.diff.logic.per_type import old_new_diff
from src.operations.project.types import ProjectData, ProjectPropertiesData
import src.operations.git.diff.renaming as renaming

def diff_properties(current: ProjectData, old_data: ProjectData | None):
	properties = ProjectPropertiesData.__annotations__.keys()
	source = current["properties"]
	old = old_data["properties"] if old_data else None
	return old_new_diff(properties,source,old,renaming.properties)