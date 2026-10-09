"""
stream/utils.py

Librería de utilidades funcionales que operan sobre Stream.
Esenciales: map, filter, reduce.
Extras: flat_map, take, drop, zip_with, sum_by, collect.
Puente Stream <-> Either: sequence, traverse.
Manejo de errores: catch, catch_each.
"""
from __future__ import annotations
from typing import Callable, TypeVar

from monads.either import Either, Left, Right
from stream.core import Stream

I = TypeVar("I")
O = TypeVar("O")
E = TypeVar("E")

#  (punto 4)                                              #

def map(stream: Stream[I], f: Callable[[I], O]) -> Stream[O]:
    """Functor: aplica f a cada elemento del stream."""
    return stream.map(f)


def filter(stream: Stream[I], pred: Callable[[I], bool]) -> Stream[I]:
    """Conserva solo los elementos que cumplen el predicado."""
    return stream.filter(pred)


def reduce(stream: Stream[I], f: Callable[[O, I], O], init: O) -> O:
    """Colapsa el stream a un único valor, partiendo de init."""
    return stream.reduce(f, init)




def flat_map(stream: Stream[I], f: Callable[[I], Stream[O]]) -> Stream[O]:
    """encadena funciones que devuelven Stream y aplana."""
    return stream.bind(f)


def take(stream: Stream[I], n: int) -> Stream[I]:
    """Primeros n elementos."""
    return stream.take(n)


def drop(stream: Stream[I], n: int) -> Stream[I]:
    """Descarta los primeros n elementos."""
    return stream.drop(n)


def zip_with(a: Stream[I], b: Stream[O], f: Callable[[I, O], E]) -> Stream[E]:
    """Combina dos streams elemento a elemento, cortando al más corto."""
    return Stream(f(x, y) for x, y in zip(a, b))


def sum_by(stream: Stream[I], key: Callable[[I], float]) -> float:
    """Suma key(x) para todo x en el stream."""
    return sum(key(x) for x in stream)


def collect(stream: Stream[Either[E, I]]) -> tuple[list[I], list[E]]:
    """
    Separa un Stream de Eithers en (rights, lefts).
    inspeccionar éxitos y errores por separado.
    """
    rights: list[I] = []
    lefts: list[E] = []
    for e in stream:
        if isinstance(e, Right):
            rights.append(e.value)
        else:
            lefts.append(e.error)
    return rights, lefts



# Puente Stream -> Either                                              #


def sequence(stream: Stream[Either[E, I]]) -> Either[E, Stream[I]]:
    """
    Stream[Either[E, I]]  ->  Either[E, Stream[I]]

    - Si TODOS son Right -> Right(Stream de valores).
    - Si ALGUNO es Left   -> Left(primer error encontrado).
    """
    values: list[I] = []
    for e in stream:
        if isinstance(e, Left):
            return Left(e.error)
        values.append(e.value)
    return Right(Stream(values))


def traverse(
    stream: Stream[I], f: Callable[[I], Either[E, O]]
) -> Either[E, Stream[O]]:
    """
    Aplica una función que puede fallar  a cada elemento.
    Equivale a sequence(stream.map(f)).
    """
    return sequence(stream.map(f))


# --------------------------------------------------------------------- #
# Manejo de errores (punto 5)                                       #
# --------------------------------------------------------------------- #

def catch(stream: Stream[I], f: Callable[[I], O]) -> Either[Exception, Stream[O]]:
    """
    Ejecuta f sobre cada elemento capturando excepciones.
    - Si todo va bien -> Right(Stream con resultados).
    - Si algo falla    -> Left(excepción). Aborta el pipeline.
    """
    try:
        return Right(Stream(f(x) for x in stream))
    except Exception as exc:
        return Left(exc)


def catch_each(
    stream: Stream[I], f: Callable[[I], O]
) -> Stream[Either[Exception, O]]:
    """
    Como catch, pero captura errores por elemento.
    Los elementos que fallan se convierten en Left(exception).
    """
    return stream.map(lambda x: Either.of(lambda: f(x)))