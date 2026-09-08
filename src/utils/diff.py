from typing import Literal
from src.operations.git.diff.types import OldNewDiff
from typing import Mapping, Any

def old_new_extractor(type: Literal["new","old"], ondiff: OldNewDiff | str) -> str | None:
    if isinstance(ondiff,str):
        return ondiff
    target = ondiff[type]
    return target if isinstance(target,str) else None

def diff_sets(source: Mapping[str, Any], old: Mapping[str, Any] | None):
    """
    Computes the set difference between source and old mappings.
    
    Args:
        source: The current/new mapping
        old: The previous mapping, or None if no previous version exists
    
    Returns:
        Tuple of (common, deleted, created) as sets of keys
    """
    source_list = set(source.keys())
    old_list = set(old.keys() if old else [])
    deleted_list = old_list - source_list
    created_list = source_list - old_list
    common_list = source_list | old_list
    return common_list, deleted_list, created_list

from src.operations.git.diff.types import OldNewDiff, VariableDiff, OldType, NewType, ActionType

def single_variable_diff(
    name: str, 
    default_old: None | OldType, default_new: None | NewType,
    type_old: None | OldType, type_new: None | NewType,
    type: ActionType
  ) -> VariableDiff:
    return {
      "name": name,
      "var_type": single_variable_diff_block(type_old,type_new,"Variable Type") if 
      type_old or type_new else None,
      "default": single_variable_diff_block(default_old,default_new,"Default Value") if 
      default_old or default_new else None,
      "change": type
    }

def single_variable_diff_block(old: OldType, new: NewType, name: str) -> OldNewDiff:
   return {"old": old, "new": new, "name": name}
