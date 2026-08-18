from src.operations.git.diff.logic.object_scope.behaviour import diff_object_behaviours
from src.operations.git.diff.logic.per_type import variable_diff
from src.operations.git.diff.types import ActionType, ObjectDiff
from src.operations.project.types import ObjectData

def diff_objects(source_objects: list[ObjectData], old_objects: list[ObjectData] | None):
	objects: list[ObjectDiff] = []
	source = {object["persistentUuid"]: object for object in source_objects}
	old = {object["persistentUuid"]: object for object in old_objects} if old_objects else None

	source_list = set(source.keys())
	old_list = set(old.keys() if old else [])
	deleted_list = old_list - source_list
	created_list = source_list - old_list
	common_list = source_list | old_list

	for uuid in common_list:
		object = source.get(uuid)
		old_object = old.get(uuid) if old else None
		is_created = uuid in created_list
		is_deleted = uuid in deleted_list
		diffType: ActionType = "Modified"
		diff = None
		name = "Unknown"

		if object:
			name = object.get("name","Unknown")
		elif old_object:
			name = old_object.get("name","Unknown")

		if not object and not is_deleted:
			continue
		
		if is_created:
			diffType = "Created"
		elif is_deleted:
			diffType = "Deleted"

		if object and not is_deleted:
			diff = diff_object(uuid,name,object,old_object)
		elif is_deleted:
			diff = diff_object(uuid,name,None,old_object)

		if diff is not None:
			diff["change"] = diffType
			objects.append(diff)

	return objects if objects else None



def diff_object(uuid: str, name: str, obj: ObjectData | None, old_obj: ObjectData | None) -> ObjectDiff | None:
	if not obj:
		return {
			"change": "Deleted",
			"variables": None,
			"behaviours": None,
			"name": name,
			"uuid": uuid
		}
	diff: ObjectDiff = {
		"variables": variable_diff(obj["variables"],old_obj["variables"] if old_obj else None),
		"change": "Modified",
		"behaviours": diff_object_behaviours(obj,old_obj),
		"name": name,
		"uuid": uuid
	}
	for s, a in diff.items():
		if a is not None and s != "change" and s != "name" and s != "uuid":
			return diff
	print("Skipped",name,uuid,diff.get("variables"))
	return None