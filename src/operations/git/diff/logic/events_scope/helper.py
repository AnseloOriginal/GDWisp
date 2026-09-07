from src.operations.project.types import CommentEventColorData


def comment_color_to_string(color: CommentEventColorData):
	return f"{color["r"]};{color["g"]};{color["b"]} {color["textR"]};{color["textG"]};{color["textB"]}"

