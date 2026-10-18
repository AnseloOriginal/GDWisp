from src.operations.project.types import InstructionData
from src.utils.string import fast_instruction_to_string
from src.utils.list import safe_get
from rapidfuzz import fuzz

def instruction_score(
	instr_a: InstructionData, 
	instr_b: InstructionData,
	instr_a_location: int,
	instr_b_location: int
):
	from src.operations.git.diff.logic.events_scope.score import location_similarity_score
	location_score = location_similarity_score(instr_a_location,instr_b_location)
	instr_a_type = instr_a.get("type").get("value")
	instr_b_type = instr_b.get("type").get("value")

	if instr_a_type != instr_b_type:
		return 0

	instr_a_str = fast_instruction_to_string(instr_a)
	instr_b_str = fast_instruction_to_string(instr_b)
	sentence_score = fuzz.ratio(instr_a_str,instr_b_str)

	return (location_score + sentence_score) / 2

def multiple_instruction_score(instrs_a: list[InstructionData],instrs_b: list[InstructionData]):
	if len(instrs_a) == 0 and len(instrs_b) == 0:
		return 100
	elif len(instrs_a) == 0 or len(instrs_b) == 0:
		return 0
	sum_score = 0
	for instr_a_index, instr_a in enumerate(instrs_a):
		scores = []
		for instr_b_index, instr_b in enumerate(instrs_b):
			location_score = instruction_score(instr_a,instr_b,instr_a_index,instr_b_index)
			non_location_score = instruction_score(instr_a,instr_b,instr_a_index,instr_a_index)
			score = (location_score+non_location_score)/2
			scores.append(score)	
			print("The score for this pass of A and B is",score)
			
		sum_score += max(scores or [0])
	return sum_score / max(len(instrs_a), len(instrs_b))





