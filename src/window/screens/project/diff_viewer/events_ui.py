from PIL.Image import new
from typing import Literal
import customtkinter as CTk
import src.core.colors as colors
from src.utils.colors import rgb_to_hex
from src.utils.diff import old_new_extractor
import src.operations.git.diff.types as diff
import src.operations.project.types as events
from src.utils.colors import string_to_comment_color

def create_event_widget(parent,event: diff.EventDiff | events.EventData):
	match event:
		case {"type": "Comment" | "BuiltinCommonInstructions::Comment"}:
			return CommentWidget(parent,event)

class BaseEventWidget(CTk.CTkFrame):
	def __init__(self,parent, **kwargs):
		super().__init__(parent, border_width=2,
			border_color="#000000",
			fg_color="#000000",
			corner_radius=0
		)

class CommentWidget(BaseEventWidget):

	def __init__(self,parent,comment: diff.CommentEventDiff | events.CommentEventData):
		super().__init__(parent)
		self.columnconfigure(0,weight=1)
		self.row = 0
		if comment["type"] == "BuiltinCommonInstructions::Comment":
			self._create_panel("existing",comment["comment"],comment["color"],True)
		else:
			comment_diff = comment["comment"]
			color_diff = comment["color"]
			if isinstance(comment_diff,str) and isinstance(color_diff,str):
				self._create_panel(
					"existing",comment_diff,string_to_comment_color(color_diff),True
				)
			else:
				new_comment = old_new_extractor("new",comment_diff)
				old_comment = old_new_extractor("old",comment_diff)
				new_color = old_new_extractor("new",color_diff)
				old_color = old_new_extractor("old",color_diff)
				general_comment = new_comment or old_comment or ""
				general_color = new_color or old_color or "0;0;0 255;255;255"
				print(
					"In order",
					(new_comment, new_color),
					(old_comment, old_color)
				)
				if old_comment or old_color:
					panel_type = "old"
					one_panel = False
					if new_comment is None and new_color is None:
						panel_type = "deleted"
						one_panel = True
					self._create_panel(
						panel_type,
						old_comment if old_comment is not None else general_comment,
						string_to_comment_color(old_color or general_color),
						one_panel
					)
				if new_comment or new_color:
					self._create_panel(
						"new",
						new_comment if new_comment is not None else general_comment,
						string_to_comment_color(new_color or general_color),
						True if old_comment is None and old_color is None else False
					)

	def _create_panel(
		self,
		type: Literal["new", "old", "existing", "deleted"], 
		comment: str,
		color: events.CommentEventColorData,
		one_panel: bool = False
	):
		readable_text = {
			"new": "NEW",
			"old": "OLD",
			"existing": "SAME",
			"deleted": "REMOVED"
		}
		color_type = {
			"new": colors.standard_diff["new"],
			"old": colors.standard_diff["old"],
			"existing": "#000000",
			"deleted": colors.standard_diff["old"]
		}
		panel = CTk.CTkFrame(self)
		panel.columnconfigure(1,weight=1)
		label = CTk.CTkLabel(
			panel,
			width=100,
			fg_color="#ffffff",
			text=readable_text[type],
			font=(None,15,"bold"),
			text_color=color_type[type]
		)
		comment_label = CTk.CTkLabel(
			panel,
			text=comment,
			fg_color=rgb_to_hex(color["r"],color["g"],color["b"]),
			text_color= rgb_to_hex(color["textR"],color["textG"],color["textB"]),
			anchor="w",
			padx=20
		)
		label.grid(column=0,row=0)
		comment_label.grid(column=1,row=0,sticky="ew")
		if self.row == 0:
			pady = (2,1)
		else:
			pady = (1,2)
		if one_panel:
			pady = 2
		panel.grid(row=self.row,column=0,sticky="ew",padx=2,pady=pady)
		self.row += 1



