from src.operations.git.diff import renaming
from src.utils.diff import diff_sets
from src.operations.git.diff.logic.per_type import old_new_diff
from src.operations.git.diff.types import ActionType, EffectDiff
from src.operations.project.types import EffectData

def flatten(effect: EffectData | None):
	if not effect:
		return None
	e: dict[str, str | float | bool] = {
		"disabled": effect.get("disabled"),
		"effectType": effect.get("effectType")
	} | {
		p: c for p, c in effect.get("doubleParameters").items()
	} | {
		p: c for p, c in effect.get("stringParameters").items()
	} | {
		p: c for p, c in effect.get("booleanParameters").items()
	}
	return e


def  diff_effects(effects: list[EffectData], old_effects: list[EffectData] | None):
	diffed_effects: list[EffectDiff] = []
	source = {e["name"]: e for e in effects}
	old = {e["name"]: e for e in old_effects} if old_effects else None

	common, deleted, created = diff_sets(source, old)

	for name in common:
		effect = source.get(name)
		old_effect = old.get(name) if old else None
		is_created = name in created
		is_deleted = name in deleted
		diffType: ActionType = "Modified"
		diff = None

		if is_created:
			diffType = "Created"
		elif is_deleted:
			diffType = "Deleted"

		if not effect and not is_deleted:
			continue
		
		if effect and not is_deleted:
			diff = diff_effect(effect,old_effect)

		diffed_effects.append({
			"name": name,
			"diff": diff,
			"change": diffType
		})

	return diffed_effects if diffed_effects else None

def diff_effect(effect_data: EffectData, old_effect_data: EffectData | None):
	effect = flatten(effect_data)
	old_effect = flatten(old_effect_data)

	if not effect:
		return
	
	diff_list = set(effect) | set(old_effect if old_effect else [])
	return old_new_diff(
		diff_list,
		effect,
		old_effect,
		renaming.effects
	)