import re
import tkinter as Tk
from typing import Literal, Sequence, Tuple
import customtkinter as CTk
from customtkinter.windows.widgets.ctk_progressbar import math
from src.operations.git.diff.logic.events_scope.metadata_scanner import MetadataScanner
import src.core.colors as colors
from src.utils.colors import rgb_to_hex
from src.utils.diff import old_new_extractor
from src.utils.list import safe_get, seq_safe_get
import src.operations.git.diff.types as diff
import src.operations.project.types as events
from src.utils.colors import string_to_comment_color
from src.utils.typing import is_base_event_diff, is_event_data, is_event_diff, is_instruction_data, is_singular_event_diff, is_instruction_diff
from src.window.screens.shared.configurable_textbox import ConfigurableTextSetting, ConfigurableTextbox

UNMODIFIED = 0
CREATED = 1
DELETED = 2
MODIFIED = 3
type Flag = Literal[0, 1, 2, 3]
EVENT_BORDER = 2

events_font: CTk.CTkFont | None = None
def create_event_widget(parent,event: diff.EventDiff | events.EventData, meta: MetadataScanner):

	global events_font
	if events_font is None:
		events_font = CTk.CTkFont(family="Inter", size=14, weight="normal")

	if is_event_diff(event) and is_base_event_diff(event):
		match event["data"]:
			case {"type": "Comment"}:
				return CommentWidget(parent,event["data"],MODIFIED)
			case {"type": "Standard Event"}:
				return StandardEventWidget(parent,event["data"],meta,MODIFIED)
	elif is_singular_event_diff(event) or is_event_data(event):
		main_event = (event["data"] if is_singular_event_diff(event) 
				else event if is_event_data(event) else None)
		e_str_type = event["diff_type"] if is_singular_event_diff(event) else "event"
		flag = CREATED if e_str_type == "created" else DELETED if e_str_type == "deleted" else UNMODIFIED
		if not main_event:
			return
		match main_event:
			case {"type": "BuiltinCommonInstructions::Comment"}:
				return CommentWidget(parent,main_event,flag)
			case {"type": "BuiltinCommonInstructions::Standard"}:
				return StandardEventWidget(parent,main_event,meta,flag)
	return None
	

class BaseEventWidget(CTk.CTkFrame):
	def __init__(self,parent, flag: Flag = 0, **kwargs):
		super().__init__(parent, border_width=2,
			height=1,
			border_color="#000000",
			corner_radius=0,
			bg_color=colors.event_sheet["bg"],
			**kwargs
		)
		self.flag_frame = CTk.CTkLabel(
			self,width=38,text_color=colors.event_sheet["icon"],
			font=("Inter",15)
		)
		self.flag_frame2 = CTk.CTkLabel(
			self,width=38,text_color=colors.event_sheet["icon"],
			font=("Inter",15)
		)
		self.flag: None | Flag = None
		self.apply_flag(flag)

	def apply_flag(self,flag: Flag,replace: CTk.CTkBaseClass | None = None, second_flag: None | Flag = None):
		self.flag = flag
		color_map = {
			MODIFIED: colors.event_sheet["modified"],
			DELETED: colors.event_sheet["removed"],
			CREATED: colors.event_sheet["added"],
			UNMODIFIED: colors.event_sheet["unmodified"]
		}
		icon_map = {
			MODIFIED: "●",
			DELETED: "-",
			CREATED: "+",
			UNMODIFIED: ""
		}
		# print("Mounting flag",color_map[flag],icon_map[flag])
		self.flag_frame.configure(bg_color=color_map[flag],text=icon_map[flag])
		self.flag_frame.grid(column=0,row=0,sticky="ns",padx=(EVENT_BORDER,0),pady=EVENT_BORDER)
		if second_flag is not None:
			self.flag_frame.grid_configure(pady=(EVENT_BORDER,0))
			self.flag_frame2.configure(bg_color=color_map[second_flag],text=icon_map[second_flag])
			self.flag_frame2.grid(column=0,row=1,sticky="ns",padx=(EVENT_BORDER,0),pady=(0,EVENT_BORDER))




class CommentWidget(BaseEventWidget):

	def __init__(
		self,
		parent,
		data: events.CommentEventData | diff.CommentEventDiff,
		flag: Flag = 0	
	):
		super().__init__(parent,flag)
		self.columnconfigure(1,weight=1)
		self.row = 0

		if data["type"] == "BuiltinCommonInstructions::Comment":
			self._create_panel(
				data["comment"],
				data["color"],True
			)
		else:
			comment_diff = data["comment"]
			color_diff = data["color"]
			new_comment = old_new_extractor("new",comment_diff)
			old_comment = old_new_extractor("old",comment_diff)
			new_color = old_new_extractor("new",color_diff)
			old_color = old_new_extractor("old",color_diff)
			general_comment = new_comment or old_comment or ""
			general_color = new_color or old_color or "0;0;0 255;255;255"

			if old_comment or old_color:
				panel_type = "old"
				one_panel = False
				self._create_panel(
					old_comment if old_comment is not None else general_comment,
					string_to_comment_color(old_color or general_color),
					one_panel
				)

			if new_comment or new_color:
				self._create_panel(
					new_comment if new_comment is not None else general_comment,
					string_to_comment_color(new_color or general_color),
					True if old_comment is None and old_color is None else False
				)
			self.apply_flag(DELETED,None,CREATED)

	def _create_panel(
		self,
		comment: str,
		color: events.CommentEventColorData,
		one_panel: bool = False
	):
		panel = CTk.CTkFrame(self)
		panel.columnconfigure(1,weight=1)
		comment_label = CTk.CTkLabel(
			panel,
			text=comment,
			fg_color=rgb_to_hex(color["r"],color["g"],color["b"]),
			text_color= rgb_to_hex(color["textR"],color["textG"],color["textB"]),
			anchor="w",
			padx=20,
			font=events_font
		)
		comment_label.grid(column=1,row=0,sticky="ew")
		if self.row == 0:
			pady = (2,1)
		else:
			pady = (1,2)
		if one_panel:
			pady = 2
		panel.grid(row=self.row,column=1,sticky="ew",padx=2,pady=pady)
		self.row += 1
		
class StandardEventWidget(BaseEventWidget):
	def __init__(self, parent, event: diff.StandardEventDiff | events.StandardEventData, meta: MetadataScanner, flag: Flag = 0, **kwargs):
		super().__init__(parent, flag, **kwargs)

		horizontal_line = Tk.Frame(self,width=1,height=1,background="black")
		actions = InstructionDiffWidget(self,event["actions"],meta,type="actions")
		conditions = InstructionDiffWidget(self,event["conditions"],meta,type="conditions")
		self.columnconfigure((1,3), weight=1, uniform="ac")
		self.rowconfigure(0, weight=1)
		horizontal_line.grid(row=0,column=2,sticky="ns", padx=10, pady=EVENT_BORDER)
		actions.grid(column=3,row=0,sticky="nsew",pady=2*EVENT_BORDER,padx=(0,EVENT_BORDER))
		conditions.grid(column=1,row=0,sticky="nsew",pady=2*EVENT_BORDER)

class InstructionDiffWidget(CTk.CTkFrame):
	def __init__(
		self, parent, 
		instructions: Sequence[diff.InstructionDiff | events.InstructionData], 
		meta: MetadataScanner, type: Literal["actions","conditions"]
	):
		super().__init__(
			parent,
			height=1,
			bg_color=colors.event_sheet["bg"]
		)
		self.instr_type: Literal["actions","conditions"] = type
		self.meta = meta
		row = 1
		self.grid_columnconfigure(0,weight=1)
		# print("Instruction",len(instructions))
		for instr in instructions:
			frame = None
			if is_instruction_diff(instr):
				frame = self.handle_instruction_diff(instr)
			if is_instruction_data(instr):
				frame = self.get_instruction_widget(instr)
			if frame:
				frame.grid(column=0,row=row,pady=(10 if row == 1 else 0,5),sticky="ew")
				row += 1


	def get_instruction_widget(
		self, 
		instr: events.InstructionData | Tuple[str,list[diff.OldNewDiff | str]],
		flag: Literal[0,1,2,3]=0
	):
		event_type = instr[0] if isinstance(instr,tuple) else instr["type"]["value"	]
		event_params = instr[1] if isinstance(instr,tuple) else instr["parameters"]
		instr_metadata = self.meta.get_instruction(event_type,self.instr_type)
		sentence = instr_metadata["sentence"] if instr_metadata else event_type
		flag_settings = self.get_flag_setting(flag)
		settings = self.get_text_settings(sentence,event_params)
		frame = CTk.CTkFrame(self)
		frame.grid_columnconfigure(1,weight=1)
		frame.grid_rowconfigure(0,weight=1)
		flag_text = CTk.CTkLabel(
			frame,
			width=40,
			text=flag_settings["text"],
			text_color=flag_settings.get("color"),
			bg_color=colors.event_sheet["bg"],
			font=("Inter",18)
		)
		textbox = ConfigurableTextbox(
			frame,settings,True,
			background=colors.event_sheet["bg"],borderwidth=0,
			foreground=colors.event_sheet["bg"],
			font=events_font,
			# state="disabled"
		)
		flag_text.grid(row=0,column=0,sticky="ns")
		textbox.grid(row=0,column=1,sticky='ew')
		return frame

	def handle_instruction_diff(self, diff: diff.InstructionDiff):
		if diff["type"] == "Modified":
			return self.get_instruction_widget(
				(diff["instr_type"],diff["parameters"]),3
			)
		else:
			return self.get_instruction_widget(
				diff["data"],
				flag=1 if diff["type" ] else 2
			)

	def get_text_settings(self,sentence: str | None, params: Sequence[str | diff.OldNewDiff])-> list[ConfigurableTextSetting]:
		sentence = "" if sentence is None else sentence
		settings: list[ConfigurableTextSetting] = []
		found_params = []
		start_index = 0
		for match in re.finditer(r"_PARAM(\d+)_",sentence):
			index = int(match.group(0).replace("_PARAM","").replace("_",""))
			found_params.append(index)

			sentence_before = sentence[start_index:match.start()]
			start_index = match.end()
			settings.append({
				"text": sentence_before
			})

			parameter = seq_safe_get(params,index)
			if parameter is None:
				settings.append({
					"text": "[NO PARAMETER]",
					"color": "red"
				})
			elif isinstance(parameter,str):
				settings.append({
					"text": parameter,
					"color": "gray"
				})
			else:
				settings = settings + self.settings_of_old_new_diff(parameter)
		remaining_sentence = sentence[start_index:]
		if len(remaining_sentence) > 0:
			settings.append({
					"text": remaining_sentence
			})
		prepend_info = True
		for (index, param) in enumerate(params):
			if index in found_params or isinstance(param,str):
				#Ignore the parameter if its in sentence or if parameter is not important (not modifide)
				continue
			if prepend_info:
				settings.append({"text": " (Extras: "})
				prepend_info = False
			settings = settings + self.settings_of_old_new_diff(param)
		if not prepend_info:
			settings.append({"text": " )"})
		return settings

	def get_flag_setting(self,flag: Flag) -> ConfigurableTextSetting:
		if flag == MODIFIED:
			return ConfigurableTextSetting(text="  ●  ",color=colors.event_sheet["modified"])
		elif flag == CREATED:
			return ConfigurableTextSetting(text="  +  ",color=colors.event_sheet["added"])
		elif flag == DELETED:
			return ConfigurableTextSetting(text="  -  ",color=colors.event_sheet["removed"])
		else:
			return ConfigurableTextSetting(text="     ")


	def settings_of_old_new_diff(self,diff: diff.OldNewDiff) -> list[ConfigurableTextSetting]:
		return [
			{
				"text": str(diff['old']),
				"color": "red"
			},
			{
				"text": " ▶ "
			},
			{
				"text": str(diff['new']),
				"color": "green"
			}
		]