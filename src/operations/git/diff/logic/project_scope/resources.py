from src.operations.git.diff import renaming
from src.operations.git.diff.logic.per_type import old_new_diff
from src.utils.diff import diff_sets
from src.operations.git.diff.types import ActionType, ResouceDiff, SceneDiff
from src.operations.project.types import ProjectData, ResourceData

def diff_resources(current: ProjectData, old_project: ProjectData | None):
	resources: list[ResouceDiff] = []
	source = {resource["name"]: resource for resource in current["resources"]["resources"]}
	old = {resource["name"]: resource for resource in old_project["resources"]["resources"]} if old_project else None

	common_list, deleted_list, created_list = diff_sets(source,old)

	for name in common_list:
		resource = source.get(name)
		old_resource = old.get(name) if old else None
		is_deleted = type in deleted_list
		is_created = type in created_list
		diffType: ActionType = "Modified"
		diff = None

		if not resource and not is_deleted:
			continue

		if is_created:
			diffType = "Created"
		elif is_deleted:
			diffType = "Deleted"

		if resource and not is_deleted:
			diff = diff_resource(resource,old_resource)

		if not diff and not is_deleted:
			continue

		resources.append({
			"change": diffType,
			"diff": diff,
			"name": name
		})

	return resources if resources else None


def diff_resource(
	resource: ResourceData,
	old_resource: ResourceData | None
):
	return old_new_diff(
		ResourceData.__annotations__,
		resource,
		old_resource,
		exclusion=["name"],
		alt_names=renaming.resources
	)




	