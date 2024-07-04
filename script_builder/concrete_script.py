from typing import List

class ConcreteScript():
    """
    It makes sense to use the Builder pattern only when your products are quite
    complex and require extensive configuration.

    Unlike in other creational patterns, different concrete builders can produce
    unrelated products. In other words, results of various builders may not
    always follow the same interface.
    """

    def __init__(self) -> None:
        self._parts: List[str] = []

    def add(self, part: str) -> None:
        self._parts.append(part)

    def list_parts(self) -> None:
        print(f"Product parts: \n {'\n'.join(self._parts)} \n")
    
    def parts_as_string(self) -> str:
        return '\n'.join(self._parts)