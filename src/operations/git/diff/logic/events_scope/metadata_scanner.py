from typing import Literal, TypedDict
from pathlib import Path
import json

from src.operations.project.types import EventsFunction, ProjectData
SCRIPT_DIR = Path(__file__).parents[6]
BUILTIN_META_PATH = SCRIPT_DIR / "data" / "gdevelop-metadata.json"

class InstructionMeta(TypedDict):
	sentence: str

class BuiltInMeta(TypedDict):
	name: str
	actions: dict[str, InstructionMeta]
	conditions: dict[str, InstructionMeta]

type BuiltInMetas = dict[str, BuiltInMeta]

class MetaStore(TypedDict):
	actions: dict[str, InstructionMeta]
	conditions: dict[str, InstructionMeta]

class MetadataScanner:
	def __init__(self):
		self.builtin_instructions = MetaStore(actions={},conditions={})
		self.project_instructions = MetaStore(actions={},conditions={})
		self.load_builtin()

	def load_builtin(self):
		try:
			as_json = BUILTIN_META_PATH.read_text()
			metas: BuiltInMetas = json.loads(as_json)
			for (name, meta) in metas.items():
				for (instr_name, instr) in meta["actions"].items():
					self.__add_to_store("builtin",instr_name,{"sentence": instr["sentence"]},"action")
				for (instr_name, instr) in meta["conditions"].items():
					self.__add_to_store("builtin",instr_name,{"sentence": instr["sentence"]},"condition")
		except OSError:
			return

	def load_project(self, project: ProjectData):
		for extension in project["eventsFunctionsExtensions"]:
			extension_name = extension["name"]
			self.handle_event_function(extension_name,extension["eventsFunctions"])
			for behaviour in extension["eventsBasedBehaviors"]:
				behaviour_name = behaviour["name"]
				name = f"{extension_name}::{behaviour_name}"
				self.handle_event_function(name,behaviour["eventsFunctions"])

	def get_instruction(self, type: str, look_in: Literal["actions","conditions"]):
		instr1 = self.builtin_instructions[look_in].get(type)
		instr2 = self.project_instructions[look_in].get(type)
		if not instr1 and not instr2:
			print("Cannot get instruction of type",type)
		return instr1 or instr2

	def handle_event_function(self,extension_name: str, ext: list[EventsFunction]):
		for instr in ext:
			if instr.get("functionType") == "Expression":
				continue
			instr_type = "action" if instr.get("functionType") == "Action" else "condition"
			instr_name = instr["name"]
			name = f"{extension_name}::{instr_name}"
			self.__add_to_store("project",name,{"sentence": instr["sentence"]},instr_type)

	def __add_to_store(
		self,
		store_type: Literal["builtin","project"], 
		instr_key: str, 
		instr: InstructionMeta, 
		instr_type: Literal["action","condition"]
	):
		store = self.builtin_instructions if store_type == "builtin" else self.project_instructions
		store_dict = store["actions"] if instr_type == "action" else store["conditions"]
		store_dict[instr_key] = instr


