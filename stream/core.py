from __future__ import annotations
from typing import Callable, Generic, Iterable, Iterator, TypeVar

I = TypeVar("I")
O = TypeVar("O")


class Stream(Generic[I]):

#guarda intermamente la tupla con los 7 diccionarios 
#y lo guardó en _items
    __slots__ = ("_items",)

    def __init__(self, source: Iterable[I]) -> None:
        self._items: tuple[I, ...] = tuple(source)

    @classmethod
    def unit(cls, value: I) -> "Stream[I]":
        return cls((value,))

    @classmethod
    def of(cls, *values: I) -> "Stream[I]":
        return cls(values)

    @classmethod
    def empty(cls) -> "Stream[I]":
        return cls(())

    def map(self, f: Callable[[I], O]) -> "Stream[O]":
        return Stream(f(x) for x in self._items)

    def apply(self, wrapped_funcs: "Stream[Callable[[I], O]]") -> "Stream[O]":
        return Stream(f(x) for f in wrapped_funcs for x in self._items)



    def bind(self, f: Callable[[I], "Stream[O]"]) -> "Stream[O]":
        return Stream(y for x in self._items for y in f(x))

    def filter(self, pred: Callable[[I], bool]) -> "Stream[I]":
        return Stream(x for x in self._items if pred(x))

    def reduce(self, f: Callable[[O, I], O], init: O) -> O:
        acc = init
        for x in self._items:
            acc = f(acc, x)
        return acc

    def take(self, n: int) -> "Stream[I]":
        return Stream(self._items[:n])

    def drop(self, n: int) -> "Stream[I]":
        return Stream(self._items[n:])

    def to_list(self) -> list[I]:
        return list(self._items)

    def __iter__(self) -> Iterator[I]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Stream) and self._items == other._items

    def __hash__(self) -> int:
        return hash(self._items)

    def __repr__(self) -> str:
        return f"Stream({list(self._items)!r})"