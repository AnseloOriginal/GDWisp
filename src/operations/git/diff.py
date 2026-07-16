from src.operations.project.types import ProjectData, ProjectPropertiesData
from typing import Any
from src.operations.git.diff_types import PropertiesDiff

class Diff:
  def __init__(self,p1: ProjectData, p2: ProjectData | None):
    #p1 is meant to be the current copy while p2 the copy from the repo
    self.p1 = p1
    self.p2 = p2
    self.__diff_properties()
  
  def __diff_properties(self):
    property_list = ProjectPropertiesData.__annotations__.keys()
    propsDiff: list[PropertiesDiff] = []
    source = self.p1["properties"]
    new = self.p2["properties"] if self.p2 else None
    for prop in property_list:
      data1 = source.get(prop)
      data2 = new.get(prop) if new else None
      if data1 == data2 or data1 == None:
        pass
      else:
        diff: PropertiesDiff = {
          "old": data2,
          "new": data1,
          "name": prop
        }
        propsDiff.append(diff)
    if (len(propsDiff) > 0):
      self.propertiesDiff = propsDiff
    else:
      self.propertiesDiff = None

  def data_as_str(self):
    data_str = []
    if self.propertiesDiff:
      data_str.append(f"Changed {len(self.propertiesDiff)} project properties")
    return data_str

  def changes_exists(self):
    p1 = self.propertiesDiff is not None
    return p1
