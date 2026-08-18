from src.operations.git.diff import helper
from src.operations.git.diff.logic.per_type import old_new_diff
from src.operations.git.diff import keys, renaming
from src.operations.git.diff.types import ActionType, LayerDiff, ObjectGroupDiff, OldNewDiff
from src.operations.project.types import LayerData, LayoutData, ObjectGroupDataObjectsType

def flatten(d: list[ObjectGroupDataObjectsType]):
  s  = "["
  for a in d:
    s += f" {a['name']},"
  s += " ]"
  return s.replace(", ]"," ]")

def diff_scene_object_groups(current_scene: LayoutData, old_scene: LayoutData | None):
  groups: list[ObjectGroupDiff] = []
  source = {group["name"]: flatten(group["objects"]) for group in current_scene["objectsGroups"]}
  old = {group["name"]: flatten(group["objects"]) for group in old_scene["objectsGroups"]} if old_scene else None
  common_list, deleted_list, created_list = helper.diff_sets(source,old)
  
  for name in common_list:
    group = source.get(name)
    old_group = old.get(name) if old else None
    is_created = name in created_list
    is_deleted = name in deleted_list
    diffType: ActionType = "Modified"
    diff: OldNewDiff | None = None

    if not group and not is_deleted:
      continue

    if is_created:
      diffType = "Created"

    if is_deleted:
      diffType = "Deleted"

    if group != old_group and not is_deleted:
      diff = {
        "name": "Objects",
        "old": old_group,
        "new": group
      }

    if not diff and not is_deleted:
      continue

    groups.append(
      {"name": name, "diff": diff, "change": diffType}
    )

  return groups if groups else None