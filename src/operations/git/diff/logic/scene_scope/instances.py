from src.utils.diff import diff_sets
from src.operations.git.diff import renaming
from src.operations.git.diff.logic.per_type import old_new_diff
from src.operations.git.diff.types import ActionType, InstanceDiff
from src.operations.project.types import InstanceData, LayoutData

def diff_scene_instances(current_scene: LayoutData, old_scene: LayoutData | None):

  instances: list[InstanceDiff] = []
  source = {instance["persistentUuid"]: instance for instance in current_scene["instances"]}
  old = {instance["persistentUuid"]: instance for instance in old_scene["instances"]} if old_scene else None
  common_list, deleted_list, created_list = diff_sets(source,old)
  
  for uuid in common_list:
    instance = source.get(uuid)
    old_instance = old.get(uuid) if old else None
    is_created = uuid in created_list
    is_deleted = uuid in deleted_list
    diffType: ActionType = "Modified"
    diff = None
    display_name = ""
    object_name = ""

    if not instance and not is_deleted:
      continue

    if is_created:
      diffType = "Created"

    if is_deleted:
      diffType = "Deleted"

    if old_instance:
      display_name = f"{old_instance['name']} ({uuid[0:6]})"
      object_name = f"{old_instance['name']}"

    if instance and not is_deleted:
      diff = diff_scene_instance(instance,old_instance)
      display_name = f"{instance['name']} ({uuid[0:6]})"
      object_name = f"{instance['name']}"

    if not diff and not is_deleted:
      continue

    instances.append(
      {
        "display_name": display_name, 
        "diff": diff, 
        "change": diffType,
        "object_name": object_name,
        "uuid": uuid
      }
    )

  return instances if instances else None

  
def diff_scene_instance(source: InstanceData, old: InstanceData | None):
  keys = InstanceData.__annotations__.keys()
  diff = old_new_diff(
    keys,
    source,
    old,
    renaming.scene_instance
  )
  return diff