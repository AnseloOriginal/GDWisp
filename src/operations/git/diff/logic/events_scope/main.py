from typing import TypeGuard
from src.operations.git.diff.logic.events_scope.events.comment import diff_comment
from src.operations.git.diff.types import EventDiff, EventStore
from src.operations.git.diff.logic.events_scope.score import similarity_score
from src.operations.project.types import CommentEventData, EventData

def diff_events(events: list[EventData], old: list[EventData] | None):
	print("-----Testing Events----")
	e: EventStore = []
	shadow_clone = old.copy() if old else []
	for event_location, event in enumerate(events):
		matched: bool = False
		diff: EventDiff | None = None
		if not old:
			# they are all new
			diff = diff_event(event,None)
			e.append(diff) if diff else None
			print(f"Found a new event {event["type"]}")
			continue
		for old_event_location, old_event in enumerate(old):
			if not old_event in shadow_clone:
				continue
			score = similarity_score(
				event,old_event,event_location,old_event_location
			)
			if score == 100:
				#We've found an exact copy
				shadow_clone.remove(old_event)
				print(f"Found an exact event {event["type"]}")
				e.append(event)
				matched = True
				break
			elif score > 75:
				# very similar so we'll take it
				diff = diff_event(event,old_event)
				shadow_clone.remove(old_event)
				matched = True
				print(f"Found a close to event {event["type"]} with score {score}")
				e.append(diff) if diff else None
		if not matched:
			# a new event
			print(f"Found a new event {event["type"]}")
			diff = diff_event(event,None)
			e.append(diff) if diff else None
			
	for old_event in shadow_clone:
		# Deleted
		print(f"Found a deleted {old_event["type"]}")
		diff = diff_event(None,old_event)
		e.append(diff) if diff else None
	return e if e else None


def is_comment_or_none(evt: EventData | None) -> TypeGuard[CommentEventData | None]:
    return evt is None or (evt is not None and evt["type"] == "BuiltinCommonInstructions::Comment")

def diff_event(new: EventData | None, old: EventData | None):
	diff: EventDiff | None = None
	if is_comment_or_none(new) and is_comment_or_none(old):
		diff = diff_comment(new,old)
	return diff
