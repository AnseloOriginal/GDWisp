from src.operations.git.diff.logic.events_scope.instructions_score import multiple_instruction_score
from src.operations.project.types import InstructionData


def create_instruction(type: str, parameters: list[str]):
	return InstructionData(type={"value": type},parameters=parameters,subInstructions=[])


def test_reliablity_of_similar_instructions_lists():
	setA = [
		create_instruction("A",["0","1","2"]),
		create_instruction("B",["3","2","1"])
	]
	setB = [
		create_instruction("A",["0","1","2"]),
		create_instruction("B",["3","2","1"])
	]
	assert multiple_instruction_score(setA,setB) == 100

def test_reliablity_of_small_changes_in_parameters():
	setA = [
		create_instruction("A",["0","1","2"]),
		create_instruction("B",["0","1","2"])
	]
	setB = [
		create_instruction("A",["0","1","2"]),
		create_instruction("B",["3","2","1"])
	]
	assert multiple_instruction_score(setA,setB) >= 75

def test_reliablity_of_instruction_reordering():
	setA = [
		create_instruction("A",["0","1","2"]),
		create_instruction("B",["3","2","1"])
	]
	setB = [
		create_instruction("B",["3","2","1"]),
		create_instruction("A",["0","1","2"])
	]
	assert multiple_instruction_score(setA,setB) >= 75

def test_reliablity_of_different_instructions():
	setA = [
		create_instruction("A",["4","5","2"]),
		create_instruction("B",["4","10","6"])
	]
	setB = [
		create_instruction("C",["3","7","1"]),
		create_instruction("D",["1","3","8"])
	]
	assert multiple_instruction_score(setA,setB) <= 75

def test_reliablity_of_empty_instructions():
	assert multiple_instruction_score([],[]) == 100

def test_reliablity_of_one_empty_instruction():
	assert multiple_instruction_score([],[create_instruction("A",["4","5","2"])]) == 0

def test_reliablity_of_wide_gap_instructions():
	setA = [
		create_instruction("A",["4","5","2"]),
	]
	setB = [
		create_instruction("A",["4","5","2"]),
		create_instruction("B",["1","2","3"]),
		create_instruction("C",["1","2","3"]),
		create_instruction("D",["1","2","3"]),
		create_instruction("E",["1","2","3"]),
	]
	assert multiple_instruction_score(setA,setB) <= 75

def test_reliablity_of_different_instructions_parameters():
	setA = [
		create_instruction("A",["5","6","7"]),
		create_instruction("B",["10","5","8"])
	]
	setB = [
		create_instruction("C",["3","7","1"]),
		create_instruction("D",["1","3","8"])
	]
	assert multiple_instruction_score(setA,setB) <= 75