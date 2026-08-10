from src.operations.git.diff_types import OldNewDiff, VariableDiff, OldType, NewType, ActionType

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