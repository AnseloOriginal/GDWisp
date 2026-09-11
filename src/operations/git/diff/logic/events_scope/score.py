from src.operations.git.diff.logic.events_scope.events.comment import comment_similarity_score
from src.operations.project.types import EventData
from rapidfuzz import fuzz

import math

def similarity_score(
	evt_a: EventData, 
	evt_b: EventData,
	evt_a_location: float,
	evt_b_location: float
):
	if evt_b["type"] != evt_a["type"]:
		return 0

	if evt_a_location == 0:
		evt_a_location = 0.00001

	if evt_b_location == 0:
		evt_b_location = 0.00001

	location_score = location_similarity_score(evt_a_location,evt_b_location)
	score = 0
	if evt_a["type"] == "BuiltinCommonInstructions::Comment" and evt_b["type"] == "BuiltinCommonInstructions::Comment":
		score = comment_similarity_score(evt_a,evt_b)

	return (location_score + score) / 2

def location_similarity_score(x: float, y: float):
	if x == y:
		return 100

	if x == 0:
		x = 0.00001

	if y == 0:
		y = 0.00001

	
	''' 
	Original formula ((100 - (abs(x-y)/x)*100) + (100 - (abs(x-y)/y)*100))/2
	Get the diff of A and B then their mean
	'''
	return round(max(100 - (50*abs(x-y)*(1/x+1/y)), 0))
