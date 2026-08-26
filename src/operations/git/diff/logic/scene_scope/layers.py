from src.operations.git.diff import helper
from src.operations.git.diff.logic.per_type import old_new_diff
from src.operations.git.diff import keys, renaming
from src.operations.git.diff.types import ActionType, LayerDiff
from src.operations.project.types import LayerData, LayoutData

def diff_scene_layers(current_scene: LayoutData, old_scene: LayoutData | None):
  layers: list[LayerDiff] = []
  source = {layer["name"]: layer for layer in current_scene["layers"]}
  old = {layer["name"]: layer for layer in old_scene["layers"]} if old_scene else None
  common_list, deleted_list, created_list = helper.diff_sets(source,old)
  
  for name in common_list:
    layer = source.get(name)
    old_layer = old.get(name) if old else None
    is_created = name in created_list
    is_deleted = name in deleted_list
    diffType: ActionType = "Modified"
    diff = None

    if not layer and not is_deleted:
      continue

    if is_created:
      diffType = "Created"

    if is_deleted:
      diffType = "Deleted"

    if layer and not is_deleted:
      diff = diff_scene_layer(layer,old_layer)

    if not diff and not is_deleted:
      continue

    layers.append(
      {"name": name, "diff": diff, "change": diffType}
    )

  return layers if layers else None

  
def diff_scene_layer(source: LayerData, old: LayerData | None):
  newpluscolor = source | {
    "ambientLightColor": helper.color_to_str(source["ambientLightColorR"],source["ambientLightColorG"],source["ambientLightColorB"])
  }
  newpluscolor["name"] = "Base Layer" if newpluscolor["name"] == "" else newpluscolor["name"]
  oldpluscolor = old | {
    "ambientLightColor": helper.color_to_str(old["ambientLightColorR"],old["ambientLightColorG"],old["ambientLightColorB"])
  } if old else None
  if oldpluscolor:
    oldpluscolor["name"] = "Base Layer" if oldpluscolor["name"] == "" else oldpluscolor["name"]
  diff = old_new_diff(
    keys.scene_layer,
    newpluscolor,
    oldpluscolor,
    renaming.scene_layer,
    ["ambientLightColorR","ambientLightColorG","ambientLightColorB"]
  )
  return diff