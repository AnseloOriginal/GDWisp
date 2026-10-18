from typing import TypeGuard, TypeIs
from src.operations.git.diff.types import BaseEventDiff, EventDiff, InstructionDiff, SingularEventDiff, SpecificEventDiff
from src.operations.project.types import CommentEventData, EventData, InstructionData, ParentEventData, StandardEventData


def is_comment(evt: EventData | None) -> TypeGuard[CommentEventData]:
    return (evt is not None and evt["type"] == "BuiltinCommonInstructions::Comment")

def is_standard_event(evt: EventData | None) -> TypeGuard[StandardEventData]:
    return (evt is not None and evt["type"] == "BuiltinCommonInstructions::Standard")


def is_event_diff(evt: EventData | EventDiff) -> TypeGuard[EventDiff]:
    return isinstance(evt.get("data"),dict) and isinstance(evt.get("diff_type"),str)

def is_event_data(evt: EventData | EventDiff) -> TypeGuard[EventData]:
    return isinstance(evt.get("type"),str)

def is_singular_event_diff(evt: EventDiff | EventData) -> TypeGuard[SingularEventDiff]:
    diff_type = evt.get("diff_type")
    return diff_type == "created" or diff_type == "deleted"

def is_base_event_diff(evt: EventDiff | EventData) -> TypeGuard[BaseEventDiff]:
    diff_type = evt.get("diff_type")
    return diff_type == "modified"

def is_instruction_diff(diff: InstructionData | InstructionDiff) -> TypeIs[InstructionDiff]:
    return isinstance(diff.get('type'),str)

def is_instruction_data(diff: InstructionData | InstructionDiff) -> TypeIs[InstructionData]:
    return not isinstance(diff.get('type'),str)
