from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar #herramientas de tipad

E = TypeVar("E") #error
I = TypeVar("I") #input 
O = TypeVar("O") #output


class Either(ABC, Generic[E, I]):
    @classmethod
    def unit(cls, v: I) -> "Either[E, I]":
        return Right(v)

    @classmethod
    def of(cls, f: Callable[[], I]) -> "Either[Exception, I]":
        try:
            return Right(f())
        except Exception as exc:
            return Left(exc)

    @abstractmethod
    def map(self, f: Callable[[I], O]) -> "Either[E, O]": ...
    @abstractmethod
    def apply(self, wf: "Either[E, Callable[[I], O]]") -> "Either[E, O]": ...
    @abstractmethod
    def bind(self, f: Callable[[I], "Either[E, O]"]) -> "Either[E, O]": ...
    @abstractmethod
    def is_right(self) -> bool: ...
    @abstractmethod
    def is_left(self) -> bool: ...
    @abstractmethod
    def get_or_else(self, default: I) -> I: ...


@dataclass(frozen=True)
class Right(Either[E, I]):
    value: I

    def map(self, f: Callable[[I], O]) -> "Either[E, O]":
        return Right(f(self.value))

    def apply(self, wf: "Either[E, Callable[[I], O]]") -> "Either[E, O]":
        return Left(wf.error) if isinstance(wf, Left) else self.map(wf.value)

    def bind(self, f: Callable[[I], "Either[E, O]"]) -> "Either[E, O]":
        return f(self.value)

    def is_right(self) -> bool:
        return True

    def is_left(self) -> bool:
        return False

    def get_or_else(self, default: I) -> I:
        return self.value


@dataclass(frozen=True)
class Left(Either[E, I]):
    error: E

    def map(self, f: Callable[[I], O]) -> "Either[E, O]":
        return self

    def apply(self, wf: "Either[E, Callable[[I], O]]") -> "Either[E, O]":
        return self

    def bind(self, f: Callable[[I], "Either[E, O]"]) -> "Either[E, O]":
        return self

    def is_right(self) -> bool:
        return False

    def is_left(self) -> bool:
        return True

    def get_or_else(self, default: I) -> I:
        return default