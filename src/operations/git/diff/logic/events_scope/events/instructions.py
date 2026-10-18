from typing import cast

from src.utils.list import safe_get
from src.operations.git.diff.types import CreatedInstructionDiff, DeletedInstructionDiff, InstructionDiff, ModifiedInstructionDiff, OldNewDiff
from src.operations.git.diff.logic.events_scope.instructions_score import instruction_score
from src.operations.project.types import InstructionData


def diff_instructions(instr_array: list[InstructionData], old_instr_array: list[InstructionData] | None) -> list[InstructionDiff | InstructionData]:
	diffs: list[InstructionDiff | InstructionData] = []
	processed_old = []
	for instr_location,instr in enumerate(instr_array):
		if not old_instr_array:
			diff = diff_instruction(instr,None)
			if diff:
				diffs.append(diff)
			continue
		matched = False
		for old_instr_location,old_instr in enumerate(old_instr_array):
			diff = None
			if old_instr in processed_old:
				continue
			score = instruction_score(
				instr,old_instr,instr_location,old_instr_location
			)
			if score == 100:
				diffs.append(instr)
				processed_old.append(old_instr)
				matched = True
				break
			elif score > 75:
				diff = diff_instruction(instr,old_instr)
				if diff:
					processed_old.append(old_instr)
			else:
				diff = diff_instruction(instr,None)
			if diff:
				diffs.append(diff)
				matched = True
		if not matched:
			diff = diff_instruction(instr,None)
			if diff:
				diffs.append(diff)
	if old_instr_array:
		for old_instr in old_instr_array:
			if not old_instr in processed_old:
				diff = diff_instruction(None,old_instr)
				if diff:
					diffs.append(diff)
	return diffs


def diff_instruction(instr: InstructionData | None, old_instr: InstructionData | None) -> InstructionDiff | None:
	if (not instr) and (not old_instr):
		return None
	if not instr and old_instr:
		return DeletedInstructionDiff(
			type = "Deleted",
			data = old_instr
		)
	if not old_instr and instr:
		return CreatedInstructionDiff(
			type = "Created",
			data = instr
		)
	if old_instr and instr:
		return ModifiedInstructionDiff(
			type = "Modified",
			parameters = diff_parameters(old_instr["parameters"],instr["parameters"]),
			sub_instructions= diff_instructions(instr.get("subInstructions") or [],old_instr.get("subInstructions")),
			instr_type = instr["type"]["value"]
		)


def diff_parameters(old: list[str], new: list[str]):
	diffs: list[OldNewDiff | str] = []
	max_index = max(len(old),len(new))
	for index in range(max_index):
		old_param = safe_get(old,index)
		new_param = safe_get(new,index)
		if isinstance(old_param,str) and old_param == new_param:
			diffs.append(old_param)
		else:
			diffs.append(
				{
					"name": str(index),
					"old": old_param,
					"new": new_param
				}
			)
	return diffs



