from src.operations.project.types import InstructionData


def fast_instruction_to_string(instr: InstructionData) -> str:
	return "Just testing "+str(instr["parameters"])