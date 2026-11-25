from src.operations.project.types import RootVariableData, VariableType
from src.operations.git.diff.types import OldNewDiff, VariableDiff, OldType, NewType, ActionType
from src.window.screens.shared.configurable_textbox import ConfigurableTextSetting
import src.core.colors as colors

def ondiff_to_text_setting(diff: OldNewDiff):
    settings: list[ConfigurableTextSetting] = []
    settings.append(
        ConfigurableTextSetting(text=str(diff["old"]))
    )
    if diff["new"] is not None:
        settings.append(
            ConfigurableTextSetting(text=" ▶ "),
        )
        settings.append(
            ConfigurableTextSetting(text=str(diff["new"]))
        )
    return settings

def variable_diff_to_text_setting(diff: list[VariableDiff] | list[RootVariableData]):
    settings: list[ConfigurableTextSetting] = []
    for var in diff:

        change_type = var["change"] if "change" in var else None
        if change_type:
            color_map: dict[ActionType,tuple[str,str]] = {
                "Modified": colors.event_sheet["modified"],
                "Deleted": colors.event_sheet["removed"],
                "Created": colors.event_sheet["added"]
            }
            icon_map: dict[ActionType,str] = {
                "Modified": "●",
                "Deleted": "-",
                "Created": "+"
            }
            settings.append(ConfigurableTextSetting(
                text=f" {icon_map.get(change_type) or "●"} ", 
                color=color_map.get(change_type)
            ))

        settings.append(ConfigurableTextSetting(text=var["name"] + " ("))

        var_type: VariableType | OldNewDiff | None = var.get("type") or var.get("var_type")
        if isinstance(var_type,str):
            settings.append(ConfigurableTextSetting(
                text=f"{" "if change_type else ""}{var_type}"
            ))
        elif var_type:
            settings += ondiff_to_text_setting(var_type)

        settings.append(ConfigurableTextSetting(text="): "))

        value: str | float | bool | None | OldNewDiff  = (
            var.get("default") if var.get("default") is not None else var.get("value")
        )
        if isinstance(value,dict):
            settings += ondiff_to_text_setting(value)
        else:
            settings.append(ConfigurableTextSetting(text=str(value)))

        # settings.append(ConfigurableTextSetting(text="\n"))
    return settings


def create_heading(text: str, colon: str = ":", gaps = 2):
    settings:list[ConfigurableTextSetting] = [
        ConfigurableTextSetting(text=text),
        ConfigurableTextSetting(text=colon)
    ]
    for i in range(gaps):
        settings.append(ConfigurableTextSetting(text="\n"))
    return settings
