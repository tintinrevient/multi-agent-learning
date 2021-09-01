# Note: Here you can put the more general functions.
# You may change everything about this file,
# but the flatten and transpose methods are used by Nash.py
# Some possibilities:
#
# A function that selects an index from a list using the values of the list as probabilities of choosing.
#
# A function that selects all indices where the maximum value occurs.
#   (Like argmax but able to return more than one index)
from typing import Iterable, Any, List


def flatten(l: Iterable[Iterable[Any]]) -> List[Any]:
    """Flatten an N dimensional iterable object to a N-1 dimensional list by removing the outer iterable."""
    return [item for sublist in l for item in sublist]


def transpose(m: Iterable[Iterable[Any]]) -> List[List[Any]]:
    """Transpose the first 2 dimensions of an iterable object with at least 2 dimensions.
    NOTE: only works when sublists are of arbitrary length."""
    return [list(i) for i in zip(*m)]
