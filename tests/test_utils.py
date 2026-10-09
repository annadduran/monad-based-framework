"""Tests de la librería de utilidades funcionales."""
import pytest

from monads import Left, Right
from stream import Stream, utils


# --------------------------------------------------------------------- #
# Esenciales                                                            #
# --------------------------------------------------------------------- #

def test_map():
    assert utils.map(Stream.of(1, 2, 3), lambda x: x * 2) == Stream.of(2, 4, 6)


def test_filter():
    s = Stream.of(1, 2, 3, 4, 5)
    assert utils.filter(s, lambda x: x > 2) == Stream.of(3, 4, 5)


def test_reduce():
    s = Stream.of(1, 2, 3, 4)
    assert utils.reduce(s, lambda a, b: a + b, 0) == 10


# --------------------------------------------------------------------- #
# Extras                                                                #
# --------------------------------------------------------------------- #

def test_flat_map():
    s = Stream.of(1, 2)
    result = utils.flat_map(s, lambda x: Stream.of(x, -x))
    assert result == Stream.of(1, -1, 2, -2)


def test_take_y_drop():
    s = Stream.of(1, 2, 3, 4, 5)
    assert utils.take(s, 2) == Stream.of(1, 2)
    assert utils.drop(s, 2) == Stream.of(3, 4, 5)


def test_zip_with():
    a = Stream.of(1, 2, 3)
    b = Stream.of(10, 20, 30)
    assert utils.zip_with(a, b, lambda x, y: x + y) == Stream.of(11, 22, 33)


def test_zip_with_corta_al_mas_corto():
    a = Stream.of(1, 2, 3)
    b = Stream.of(10, 20)
    assert utils.zip_with(a, b, lambda x, y: x + y) == Stream.of(11, 22)


def test_sum_by():
    s = Stream.of(1, 2, 3)
    assert utils.sum_by(s, lambda x: x ** 2) == 14


def test_collect_separa_rights_y_lefts():
    s = Stream.of(Right(1), Left("e1"), Right(2), Left("e2"))
    rights, lefts = utils.collect(s)
    assert rights == [1, 2]
    assert lefts == ["e1", "e2"]


# --------------------------------------------------------------------- #
# Puente Stream <-> Either                                              #
# --------------------------------------------------------------------- #

def test_sequence_todos_right():
    s = Stream.of(Right(1), Right(2), Right(3))
    result = utils.sequence(s)
    assert result.is_right()
    assert result.value == Stream.of(1, 2, 3)


def test_sequence_con_un_left_devuelve_primer_error():
    s = Stream.of(Right(1), Left("e1"), Left("e2"))
    assert utils.sequence(s) == Left("e1")


def test_traverse_camino_feliz():
    result = utils.traverse(Stream.of(1, 2, 4), lambda x: Right(100 / x))
    assert result.is_right()
    assert result.value == Stream.of(100.0, 50.0, 25.0)


def test_traverse_con_fallo():
    safe_div = lambda x: Left("div0") if x == 0 else Right(100 / x)
    assert utils.traverse(Stream.of(1, 0, 2), safe_div) == Left("div0")


# --------------------------------------------------------------------- #
# Manejo de errores                                                     #
# --------------------------------------------------------------------- #

def test_catch_camino_feliz():
    result = utils.catch(Stream.of(1, 2, 4), lambda x: 100 / x)
    assert result.is_right()
    assert result.value == Stream.of(100.0, 50.0, 25.0)


def test_catch_detecta_excepcion():
    result = utils.catch(Stream.of(1, 0, 2), lambda x: 100 / x)
    assert result.is_left()
    assert isinstance(result.error, ZeroDivisionError)


def test_catch_each_marca_errores_individuales():
    result = utils.catch_each(Stream.of(1, 0, 4), lambda x: 100 / x).to_list()
    assert result[0] == Right(100.0)
    assert result[1].is_left()
    assert isinstance(result[1].error, ZeroDivisionError)
    assert result[2] == Right(25.0)