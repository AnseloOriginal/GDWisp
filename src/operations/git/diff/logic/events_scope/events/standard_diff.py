from src.operations.git.diff.logic.events_scope.events.instructions import diff_instructions
from src.operations.git.diff.types import StandardEventDiff
from src.operations.git.diff.logic.events_scope.instructions_score import multiple_instruction_score
from src.operations.project.types import StandardEventData
from src.utils.diff import context_aware_variable_diff

def standard_event_similarity_score(evtA: StandardEventData, evtB: StandardEventData):
	actions = multiple_instruction_score(evtA["actions"],evtB["actions"])
	conditions = multiple_instruction_score(evtA["conditions"],evtB["conditions"])
	return (actions + conditions) / 2

def standard_diff(evtA: StandardEventData, evtB: StandardEventData):
	actions = diff_instructions(evtA["actions"],evtB["actions"])
	conditions = diff_instructions(evtA["conditions"],evtB["conditions"])
	variables = context_aware_variable_diff(evtA.get("variables"),evtB.get("variables"))
	return StandardEventDiff(
		actions=actions,
		conditions=conditions,
		type="Standard Event",
		variables=variables
	)
