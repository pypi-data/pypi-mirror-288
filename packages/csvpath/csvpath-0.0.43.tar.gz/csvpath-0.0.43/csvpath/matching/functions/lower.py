from typing import Any
from .function import Function, ChildrenException


class Lower(Function):
    def to_value(self, *, skip=[]) -> Any:
        if self in skip:
            return True
        if len(self.children) != 1:
            self.matcher.print(
                f"Lower.to_value: must have 1 equality child: {self.children}"
            )
            raise ChildrenException("Lower function must have 1 child")

        value = self.children[0].to_value(skip=skip)
        value = f"{value}".lower()
        return value

    def matches(self, *, skip=[]) -> bool:
        v = self.to_value(skip=skip)
        return v is not None
