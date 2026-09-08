from src.operations.project.types import ProjectData
from src.operations.git.diff.logic.scene_scope.main import diff_scenes
from src.operations.git.diff.logic.project_scope.resources import diff_resources
from src.operations.git.diff.logic.project_scope.project_properties import diff_properties
from src.operations.git.diff.logic.project_scope.global_variables import global_variable_diff




class Diff:
  def __init__(self,p1: ProjectData, p2: ProjectData | None):
    # p1 is meant to be the current copy while 
    # p2 the copy from the repo (which may not exists)
    self.p1 = p1
    self.p2 = p2

    self.globalVarDiff = global_variable_diff(p1,p2)
    self.propertiesDiff = diff_properties(p1,p2)
    self.scene_diffs = diff_scenes(p1,p2)
    self.resourcesDiff = diff_resources(p1,p2)
  
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
