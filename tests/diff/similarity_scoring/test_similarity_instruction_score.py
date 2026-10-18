from src.operations.git.diff.logic.events_scope.instructions_score import instruction_score
from src.operations.project.types import InstructionData


def test_instruction_similarity_score_different_instruction():
	instr1: InstructionData = {
		"type": {
			"value": "InstrTypeA"
		},
		"parameters": [],
		"subInstructions": []
	}
	instr2: InstructionData = {
		"type": {
			"value": "InstrTypeB"
		},
		"parameters": [],
		"subInstructions": []
	}

	assert instruction_score(instr1,instr2,1,1) == 0

def test_instruction_similarity_score_same_instruction():
	instr1: InstructionData = {
		"type": {
			"value": "InstrTypeA"
		},
		"parameters": [],
		"subInstructions": []
	}
	instr2: InstructionData = {
		"type": {
			"value": "InstrTypeA"
		},
		"parameters": [],
		"subInstructions": []
	}

	assert instruction_score(instr1,instr2,1,1) == 100


def test_instruction_similarity_score_with_parameters():
	instr1: InstructionData = {
		"type": {
			"value": "InstrTypeA"
		},
		"parameters": ["Bella"],
		"subInstructions": []
	}
	instr2: InstructionData = {
		"type": {
			"value": "InstrTypeA"
		},
		"parameters": ["Hellos"],
		"subInstructions": []
	}
	score = instruction_score(instr1,instr2,1,1)
	assert score > 75 and score < 100