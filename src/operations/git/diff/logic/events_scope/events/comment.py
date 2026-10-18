import rapidfuzz
from rapidfuzz import fuzz
from src.utils.colors import comment_color_to_string
from src.operations.git.diff.logic.per_type import diff_strings
from src.operations.git.diff.types import ActionType, CommentEventDiff
from src.operations.project.types import CommentEventColorData, CommentEventData


def to_color(color: CommentEventColorData | None):
	if color:
		return comment_color_to_string(color)
	else:
		return None

def comment_similarity_score(evt_a: CommentEventData, evt_b: CommentEventData):
	evt_a_map = f"{comment_color_to_string(evt_a["color"])} {evt_a["comment"]}"
	evt_b_map = f"{comment_color_to_string(evt_b["color"])} {evt_b["comment"]}"
	score = fuzz.ratio(evt_a_map, evt_b_map)
	return score

#Evt_b acts as old while Evt_a as new/source_
def diff_comment(evt_a: CommentEventData, evt_b: CommentEventData):

	comment_string_diff = diff_strings(
		"Comment",
		evt_a["comment"] if evt_a else None,
		evt_b["comment"] if evt_b else None
	)

	comment_color_diff = diff_strings(
		"Color",
		to_color(evt_a["color"] if evt_a else None),
		to_color(evt_b["color"] if evt_b else None)
	)
	comment = evt_a["comment"] if evt_a else evt_b["comment"] if evt_b else ""
	color = comment_color_to_string(evt_a["color"]) if evt_a else comment_color_to_string(evt_b["color"]) if evt_b else ""

	return CommentEventDiff(
		type="Comment",
		comment= comment_string_diff if comment_string_diff else comment,
		color= comment_color_diff if comment_color_diff else color
	)