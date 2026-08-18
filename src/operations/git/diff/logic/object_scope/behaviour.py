from typing import Any
from src.operations.git.diff import helper
from src.operations.git.diff.logic.per_type import old_new_diff
from src.operations.git.diff.types import ActionType, BehaviourDiff
from src.operations.project.types import BehaviorData, ObjectData

def diff_object_behaviours(obj: ObjectData, old_obj: ObjectData | None):
    behaviours: list[BehaviourDiff] = []
    source = {obj["type"]: obj for obj in obj["behaviors"]}
    old = {obj["type"]: obj for obj in old_obj["behaviors"]} if old_obj else None
    common_list, deleted_list, created_list = helper.diff_sets(source,old)

    for type in common_list:
        behaviour = source.get(type)
        old_behaviour = old.get(type) if old else None
        is_deleted = type in deleted_list
        is_created = type in created_list
        diffType: ActionType = "Modified"
        diff = None

        name = type if isinstance(type,str) else "Unknown"
        if behaviour:
            prename = behaviour.get("name")
            name = prename if isinstance(prename,str) else name
        elif old_behaviour:
            prename = old_behaviour.get("name")
            name = prename if isinstance(prename,str) else name

        if not behaviour and not is_deleted:
            print(f"Skipping Behaviour {name} due to noexistent")
            continue

        if is_created:
            diffType = "Created"
        elif is_deleted:
            diffType = "Deleted"

        if behaviour and not is_deleted:
            diff = diff_behaviour(behaviour,old_behaviour)

        if not diff and not is_deleted:
            print(f"Skipping Behaviour {name} due to no-diff")
            continue

        behaviours.append({
            "change": diffType,
            "diff": diff,
            "name": name
        })

    return behaviours if behaviours else None


def diff_behaviour(
    behaviour: BehaviorData | dict[str, Any],
    old_behaviour: BehaviorData | dict[str, Any] | None
):
    properties = set(behaviour)
    print("Behaviour",properties)
    if old_behaviour:
        properties = properties | set(old_behaviour)
    return old_new_diff(
        properties,
        behaviour,
        old_behaviour,
        exclusion=["type"]
    )
