from abc import ABC, abstractmethod

from ..concrete_script import ConcreteScript

class CreateScript(ABC):
    """
    The Abstract Class defines a template method that contains a skeleton of
    some algorithm, composed of calls to (usually) abstract primitive
    operations.

    Concrete subclasses should implement these operations, but leave the
    template method itself intact.
    """

    def __init__(self) -> None:
        self._script = ConcreteScript()

    def get_script(self) -> ConcreteScript:
        return self._script

    # These operations already have implementations.

    def add_create_packague(self, packague_name: str) -> None:
        self._script.add("mkdir "+packague_name)

    def add_line_break(self) -> None:
        self._script.add("\n")

    # These operations have to be implemented in subclasses.

    @abstractmethod
    def add_comment(self, comment: str) -> None:
        pass
    
    @abstractmethod
    def add_print(self) -> None:
        pass
    
    @abstractmethod
    def add_enter_project_packague(self) -> None:
        pass
    
    @abstractmethod
    def add_command(self) -> None:
        pass
    
    @abstractmethod
    def add_create_file(self) -> None:
        pass
    
    @abstractmethod
    def add_write_to_file(self) -> None:
        pass
