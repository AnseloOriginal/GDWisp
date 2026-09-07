from src.operations.git.diff.types import OldNewDiff


def diff_strings(name: str, new: str | None, old: str | None):
	if old == new:
		return None
	diff: OldNewDiff = {
		"old": old,
		"new": new,
		"name": name
	}
	return diff
