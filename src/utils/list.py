from collections.abc import Sequence


def safe_get[T, D](lst: list[T], index: int, default: D = None) -> T | D:
    try:
        return lst[index]
    except IndexError:
        return default

def seq_safe_get[T, D](seq: Sequence[T], index: int, default: D = None) -> T | D:
    try:
        return seq[index]
    except IndexError:
        return default

def general_safe_get(seq, index, default=None):
    try:
        return seq[index]
    except (TypeError, IndexError, KeyError):
        return default