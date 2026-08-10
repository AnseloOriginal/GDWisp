from src.operations.project.types import ProjectData, ProjectPropertiesData, LayoutData, RootVariableData
from typing import Any, Iterable, Mapping, Union, Literal
from src.operations.git.diff_types import OldNewDiff, SceneDiff, VariableDiff, OldType, NewType, ActionType
import src.operations.git.diff_renaming as renaming
import src.operations.git.diff_helper as helper

class Diff:
  def __init__(self,p1: ProjectData, p2: ProjectData | None):
    #p1 is meant to be the current copy while p2 the copy from the repo
    self.p1 = p1
    self.p2 = p2
    self.scene_diffs: dict[str, SceneDiff] = {}
    self.diff_project()
    self.diff_scenes()
    

  def diff_project(self):
    self.diff_properties()
    self.diff_global_variables()

  def diff_scenes(self):
    source = {scene["name"]: scene for scene in self.p1["layouts"]}
    old = {scene["name"]: scene for scene in self.p2["layouts"]} if self.p2 else None
    for name, scene in source.items():
      old_scene = old.get(name) if old else None

      scene_diff: SceneDiff = {
        "properties": self.diff_scene_properties(scene,old_scene),
        "variables": self.diff_scene_variables(scene,old_scene)
      }
      for s, a in scene_diff.items():
        if a is None:
          continue
        self.scene_diffs[name] = scene_diff
        break

  def diff_scene_variables(self, source: LayoutData, old: LayoutData | None):
    return self.variable_diff(
      source["variables"],
      old["variables"] if old else None
    )


  def diff_scene_properties(self, source: LayoutData, old: LayoutData | None):
    newpluscolor = source | {
      "color": self.color_to_str(source["r"],source["v"],source["b"])
    }
    oldpluscolor = old | {
      "color": self.color_to_str(old["r"],old["v"],old["b"])
    } if old else None
    diff = self.old_new_diff(
      ["color","stopSoundsOnStartup","title","resourcePreloading","resourceUnloading",
        "disableInputWhenNotFocused"
      ],
      newpluscolor,
      oldpluscolor,
      renaming.scene_variables
    )
    return diff

  def diff_properties(self):
    properties = ProjectPropertiesData.__annotations__.keys()
    source = self.p1["properties"]
    new = self.p2["properties"] if self.p2 else None
    self.propertiesDiff = self.old_new_diff(properties,source,new,renaming.properties)

  def diff_global_variables(self):
    self.globalVarDiff = self.variable_diff(
      self.p1["variables"],
      self.p2["variables"] if self.p2 else None
    )

  def variable_diff(
    self,
    current_list: list[RootVariableData],
    old_list: list[RootVariableData] | None,
  ):
    diffs: list[VariableDiff] = []
    current = {item["name"]: item for item in current_list}
    old = {item["name"]: item for item in old_list} if old_list else {}
    processed: list[str] = []
    for var_name, var in current.items():
      old_var = old.get(var_name)
      processed.append(var_name)
      if old_var is None:
        diff = helper.single_variable_diff(
          var_name, None, var.get("value",0), None, var["type"],"Created"
        )
        diffs.append(diff)
      else:
        typeDiff: OldNewDiff | None = None
        defaultDiff: OldNewDiff | None = None

        if var["type"] != old_var["type"]:
          typeDiff = helper.single_variable_diff_block(
            old_var["type"],  var["type"],  "Variable Type"
          )
          
        if var.get("value",0) != old_var.get("value",0):
          defaultDiff = helper.single_variable_diff_block(
            old_var.get("value",0),  var.get("value",0),  "Default Value"
          )

        if not (typeDiff or defaultDiff):
          continue

        diff: VariableDiff = {
          "name": var_name,
          "var_type": typeDiff,
          "default": defaultDiff,
          "change": "Modified"
        }
        diffs.append(diff)
    if old:
      for var_name, var in old.items():
        if var_name in processed:
          continue
        d = "Deleted"
        diff = helper.single_variable_diff(
          var_name,var.get("value",0) , d, var["type"], d, "Deleted"
        )
        diffs.append(diff)
        
    return diffs if diffs else None
  

  def old_new_diff(
    self, 
    keys: Iterable[str],
    source: Mapping[str, Any],
    new: Mapping[str, Any] | None,
    alt_names: dict[str, str] = {}
  ):
    ONdiff: list[OldNewDiff] = []
    for key in keys:
      data1 = source.get(key)
      data2 = new.get(key) if new else None
      if data1 == data2 or data1 == None:
        pass
      else:
        alt_name = alt_names.get(key)
        diff: OldNewDiff = {
          "old": data2,
          "new": data1,
          "name": alt_name if alt_name else key
        }
        ONdiff.append(diff)

    return ONdiff if ONdiff else None

  def color_to_str(self,r: int, g: int, b: int):
    return f"{r}; {g}; {b}"


  def data_as_str(self):
    data_str = []
    if self.propertiesDiff:
      data_str.append(f"Changed {len(self.propertiesDiff)} project properties")
    if self.globalVarDiff:
      data_str.append(f"Changed {len(self.globalVarDiff)} global variables")
    if len(self.scene_diffs) > 0:
      data_str.append(f"Modified {len(self.scene_diffs)} scenes")

    return data_str

  def changes_exists(self):
    t1 = self.propertiesDiff is not None
    t2 = self.globalVarDiff is not None
    t3 = len(self.scene_diffs) > 0
    return t1 or t2 or t3
