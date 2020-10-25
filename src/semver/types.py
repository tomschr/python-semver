from typing import Callable, Collection, Dict, Iterator, Optional, Tuple, TypeVar, Union


# Types
VersionPart = Union[int, Optional[str]]
Comparable = Union["VersionInfo", Dict[str, VersionPart], Collection[VersionPart], str]
Comparator = Callable[["VersionInfo", Comparable], bool]
String = Union[str, bytes]
VersionTuple = Tuple[int, int, int, Optional[str], Optional[str]]
VersionDict = Dict[str, VersionPart]
VersionIterator = Iterator[VersionPart]

F = TypeVar("F", bound=Callable)
