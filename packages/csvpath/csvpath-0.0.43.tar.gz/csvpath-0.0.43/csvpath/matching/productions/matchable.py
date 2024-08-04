from typing import Any, Self, Optional
from csvpath.matching.expression_utility import ExpressionUtility

# from ..expression_encoder import ExpressionEncoder
from enum import Enum


class Qualities(Enum):
    ONMATCH = "onmatch"
    IFEMPTY = "ifempty"
    ONCHANGE = "onchange"
    ASBOOL = "asbool"
    NOCONTRIB = "nocontrib"


class Matchable:
    QUALIFIERS = [
        Qualities.ONMATCH.value,
        Qualities.IFEMPTY.value,
        Qualities.ONCHANGE.value,
        Qualities.ASBOOL.value,
        Qualities.NOCONTRIB.value,
    ]

    def __init__(self, matcher, *, value: Any = None, name: str = None):
        self.parent = None
        self.children = []
        self.matcher = matcher
        self.value = value
        self.match = None  # holds the value of matches() if needed by the function
        self.name = name
        self._id: str = None
        if self.name and self.name.__class__ == str:
            self.name = self.name.strip()
        self.qualifier = None
        if name is None:
            self.qualifiers = []
        else:
            n, qs = ExpressionUtility.get_name_and_qualifiers(name)
            self.name = n
            self.qualifiers = qs

    def __str__(self) -> str:
        return f"""{self.__class__}"""

    def first_non_term_qualifier(self, default: None) -> Optional[str]:
        if not self.qualifiers:  # this shouldn't happen but what if it did
            return default
        for q in self.qualifiers:
            if q not in Matchable.QUALIFIERS:
                return q
        return default

    def set_qualifiers(self, qs) -> None:
        self.qualifier = qs
        if qs is not None:
            self.qualifiers = qs.split(".")

    def has_onmatch(self) -> bool:
        if self.qualifiers:
            return Qualities.ONMATCH.value in self.qualifiers
        return False

    def has_ifempty(self) -> bool:
        if self.qualifiers:
            return Qualities.IFEMPTY.value in self.qualifiers
        return False

    def has_onchange(self) -> bool:
        if self.qualifiers:
            return Qualities.ONCHANGE.value in self.qualifiers
        return False

    def has_asbool(self) -> bool:
        if self.qualifiers:
            return Qualities.ASBOOL.value in self.qualifiers
        return False

    def has_nocontrib(self) -> bool:
        if self.qualifiers:
            return Qualities.NOCONTRIB.value in self.qualifiers
        return False

    @property
    def nocontrib(self) -> bool:
        return self.has_nocontrib()

    @property
    def asbool(self) -> bool:
        return self.has_asbool()

    @property
    def onmatch(self) -> bool:
        return self.has_onmatch()

    @property
    def onchange(self) -> bool:
        return self.has_onchange()

    @onchange.setter
    def onchange(self, oc: bool) -> None:
        if Qualities.ONCHANGE.value not in self.qualifiers:
            self.qualifiers.append(Qualities.ONCHANGE.value)

    def line_matches(self):
        es = self.matcher.expressions
        for e in es:
            m = e[0].matches(skip=[self])
            if not m:
                return False
        return True

    def reset(self) -> None:
        # let the subclasses handle value
        # self.value = None
        for child in self.children:
            child.reset()

    def matches(self, *, skip=[]) -> bool:
        return True  # leave this for now for testing

    def to_value(self, *, skip=[]) -> Any:
        return None

    def index_of_child(self, o) -> int:
        return self.children.index(o)

    def set_parent(self, parent: Self) -> None:
        self.parent = parent

    def add_child(self, child: Self) -> None:
        if child:
            child.set_parent(self)
            if child not in self.children:
                self.children.append(child)

    def get_id(self, child: Self = None) -> str:
        if not self._id:
            thing = self if not child else child
            self._id = ExpressionUtility.get_id(thing=thing)
        return self._id
