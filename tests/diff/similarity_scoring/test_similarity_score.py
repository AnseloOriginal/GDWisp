from src.operations.project.types import EventData
import src.operations.git.diff.logic.events_scope.score as score


def test_similarity_score_same_comment_events():
	comment: EventData = {
		"type": "BuiltinCommonInstructions::Comment",
		"comment": "Hello",
		"color": {
			"r": 255,
			"g": 255,
			"b": 255,
			"textR": 255,
			"textG": 255,
			"textB": 255
		}
	}
	assert score.similarity_score(comment,comment,10,10) == 100

def test_similarity_score_different_comment_events():
	comment1: EventData = {
		"type": "BuiltinCommonInstructions::Comment",
		"comment": "Hello",
		"color": {
			"r": 255,
			"g": 255,
			"b": 255,
			"textR": 255,
			"textG": 255,
			"textB": 255
		}
	}
	comment2: EventData = {
		"type": "BuiltinCommonInstructions::Standard",
		"actions": [],
		"conditions": []
	}
	assert score.similarity_score(comment1,comment2,10,10) == 0

def test_location_score_equality():
	assert score.location_similarity_score(10,10) == 100

def test_location_score_reliability():
	assert score.location_similarity_score(10,20) == 25

def test_location_score_both_zero():
	assert score.location_similarity_score(0,0) == 100

def test_location_score_one_zero():
	assert score.location_similarity_score(0,10) == 0