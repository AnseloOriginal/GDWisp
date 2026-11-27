import math

from src.operations.project.types import InstructionData


def fast_instruction_to_string(instr: InstructionData) -> str:
	return "Just testing "+str(instr["parameters"])

def center_padding(size: int = 3, char: str = ""):
	if char:
		side_size = math.floor(size/2)
		return (" "*side_size) + char + (" "*side_size)
	else:
		return " "*size