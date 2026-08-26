from src.operations.git.diff.logic.object_scope.effects import diff_effects
from src.operations.git.diff import helper
from src.operations.git.diff.logic.object_scope.behaviour import diff_object_behaviours
from src.operations.git.diff.logic.per_type import variable_diff
from src.operations.git.diff.types import ActionType, ObjectDiff
from src.operations.project.types import ObjectData

def diff_objects(source_objects: list[ObjectData], old_objects: list[ObjectData] | None):
	objects: list[ObjectDiff] = []
	source = {object["persistentUuid"]: object for object in source_objects}
	old = {object["persistentUuid"]: object for object in old_objects} if old_objects else None
	common_list, deleted_list, created_list = helper.diff_sets(source,old)

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
			"effects": None,
			"name": name,
			"uuid": uuid
		}
	diff: ObjectDiff = {
		"variables": variable_diff(obj["variables"],old_obj["variables"] if old_obj else None),
		"change": "Modified",
		"behaviours": diff_object_behaviours(obj,old_obj),
		"effects": diff_effects(
			obj.get("effects"),
			old_obj.get("effects") if old_obj else None
		),
		"name": name,
		"uuid": uuid
	}
	for s, a in diff.items():
		if a is not None and s != "change" and s != "name" and s != "uuid":
			return diff
	return None