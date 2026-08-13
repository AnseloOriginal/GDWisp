from src.operations.git.diff.logic.scene_scope.instances import diff_scene_instances
from src.operations.git.diff.logic.scene_scope.layers import diff_scene_layers
from src.operations.git.diff.logic.scene_scope.properties import diff_scene_properties
from src.operations.git.diff.logic.scene_scope.variables import diff_scene_variables
from src.operations.project.types import ProjectData
from src.operations.git.diff.types import SceneDiff


def diff_scenes(source_data: ProjectData, old_data: ProjectData | None):

  diff: dict[str, SceneDiff] = {}
  source = {scene["name"]: scene for scene in source_data["layouts"]}
  old = {scene["name"]: scene for scene in old_data["layouts"]} if old_data else None
  for name, scene in source.items():
    old_scene = old.get(name) if old else None

    scene_diff: SceneDiff = {
      "properties": diff_scene_properties(scene,old_scene),
      "variables": diff_scene_variables(scene,old_scene),
      "layers": diff_scene_layers(scene,old_scene),
      "instances": diff_scene_instances(scene,old_scene)
    }
    for s, a in scene_diff.items():
       if a is None:
         continue
    diff[name] = scene_diff
  return diff
    