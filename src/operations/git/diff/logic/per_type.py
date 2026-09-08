from src.operations.project.types import RootVariableData
from src.operations.git.diff.types import OldNewDiff, VariableDiff
from src.utils.diff import single_variable_diff, single_variable_diff_block
from typing import Any, Iterable, Mapping


def old_new_diff(
    keys: Iterable[str],
    source: Mapping[str, Any],
    new: Mapping[str, Any] | None,
    alt_names: dict[str, str] = {},
    exclusion: list[str] = []
):
    ONdiff: list[OldNewDiff] = []
    for key in keys:
      if key in exclusion:
        continue
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

def diff_strings(name: str, new: str | None, old: str | None):
    if old == new:
        return None
    diff: OldNewDiff = {
        "old": old,
        "new": new,
        "name": name
    }
    return diff


def variable_diff(
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
        diff = single_variable_diff(
          var_name, None, var.get("value",0), None, var["type"],"Created"
        )
        diffs.append(diff)
      else:
        typeDiff: OldNewDiff | None = None
        defaultDiff: OldNewDiff | None = None

        if var["type"] != old_var["type"]:
          typeDiff = single_variable_diff_block(
            old_var["type"],  var["type"],  "Variable Type"
          )
          
        if var.get("value",0) != old_var.get("value",0):
          defaultDiff = single_variable_diff_block(
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
        diff = single_variable_diff(
          var_name,var.get("value",0) , d, var["type"], d, "Deleted"
        )
        diffs.append(diff)

    return diffs if diffs else None
