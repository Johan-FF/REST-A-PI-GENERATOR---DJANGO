from abc import ABC, abstractmethod

class Builder(ABC):
    """
    The Builder interface specifies methods for creating the different parts of
    the Scripts objects.
    """

    @property
    @abstractmethod
    def script(self) -> None:
        pass

    @abstractmethod
    def produce_crud(self) -> None:
        pass

    @abstractmethod
    def produce_create(self) -> None:
        pass

    @abstractmethod
    def produce_read(self) -> None:
        pass

    @abstractmethod
    def produce_update(self) -> None:
        pass

    @abstractmethod
    def produce_delete(self) -> None:
        pass