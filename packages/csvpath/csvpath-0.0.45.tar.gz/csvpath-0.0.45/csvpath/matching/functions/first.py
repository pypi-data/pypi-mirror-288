from typing import Any
from .function import Function, ChildrenException
from ..productions import Equality


class First(Function):
    NEVER = -9999999999

    def __init__(self, matcher, name: str = None, child: Any = None):
        super().__init__(matcher, child=child, name=name)
        self._my_value_or_none = First.NEVER  # when this var is None we match

    def reset(self) -> None:
        super().reset()
        self._my_value_or_none = First.NEVER

    def to_value(self, *, skip=[]) -> Any:
        if self in skip:
            return self._my_value_or_none
        if len(self.children) != 1:
            self.matcher.print(f"First.to_value: must have 1 child: {self.children}")
            raise ChildrenException("First function must have 1 child")
        if self._my_value_or_none == First.NEVER:
            om = self.has_onmatch()
            if not om or self.line_matches():

                child = self.children[0]
                value = ""
                if isinstance(child, Equality):
                    for _ in child.commas_to_list():
                        value += f"{_.to_value(skip=skip)}"
                else:
                    value = f"{child.to_value(skip=skip)}"
                value = value.strip()
                my_id = self.first_non_term_qualifier(self.name)

                v = self.matcher.get_variable(my_id, tracking=value)
                if v is None:
                    self.matcher.set_variable(
                        my_id,
                        tracking=value,
                        value=self.matcher.csvpath.current_line_number(),
                    )
                #
                # when we have no earlier value we are first, so we match
                #
                self._my_value_or_none = v
        return self._my_value_or_none

    def matches(self, *, skip=[]) -> bool:
        if self in skip:
            return True
        om = self.has_onmatch()
        if om and not self.line_matches():
            ret = False
        else:
            #
            # when there is no earlier value we match
            #
            if self._my_value_or_none == First.NEVER:
                self.to_value(skip=skip)
            v = self._my_value_or_none
            ret = v is None
        return ret
