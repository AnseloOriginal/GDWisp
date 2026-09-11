from src.operations.git.diff.logic.events_scope.score import location_similarity_score
from src.operations.project.types import InstructionData
from src.utils.string import fast_instruction_to_string
from rapidfuzz import fuzz

def instruction_score(
	instr_a: InstructionData, 
	instr_b: InstructionData,
	instr_a_location: int,
	instr_b_location: int
):
	location_score = location_similarity_score(instr_a_location,instr_b_location)
	instr_a_type = instr_a.get("type").get("type")
	instr_b_type = instr_b.get("type").get("type")

	if instr_a_type != instr_b_type:
		return 0

	instr_a_str = fast_instruction_to_string(instr_a)
	instr_b_str = fast_instruction_to_string(instr_b)
	sentence_score = fuzz.ratio(instr_a_str,instr_b_str)

	return (location_score + sentence_score) / 2
