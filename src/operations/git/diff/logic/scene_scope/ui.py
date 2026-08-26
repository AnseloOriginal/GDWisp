from src.operations.git.diff import renaming
from src.operations.git.diff.logic.per_type import old_new_diff
from src.operations.project.types import InstancesEditorSettings, LayoutData


def diff_scene_ui(scene: LayoutData, old_scene: LayoutData | None):
	diff_list = InstancesEditorSettings.__annotations__

	return old_new_diff(
		diff_list,
		scene.get("uiSettings"),
		old_scene.get("uiSettings") if old_scene else None,
		renaming.uisettings
	)