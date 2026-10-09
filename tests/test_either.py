import pytest

from monads import Either, Left, Right


# Constructores                                                         #


def test_unit_envuelve_en_right():
    assert Either.unit(5) == Right(5)


def test_of_captura_excepcion():
    result = Either.of(lambda: 1 / 0)
    assert result.is_left()
    assert isinstance(result.error, ZeroDivisionError)


def test_of_camino_feliz():
    assert Either.of(lambda: 42) == Right(42)



# Functor (map)                                                         #


def test_map_sobre_right():
    assert Right(5).map(lambda x: x * 2) == Right(10)


def test_map_sobre_left_es_noop():
    assert Left("err").map(lambda x: x * 2) == Left("err")



# Applicative (apply)                                                   #


def test_apply_right_con_right():
    wf = Right(lambda x: x + 1)
    assert Right(5).apply(wf) == Right(6)


def test_apply_right_con_left_propaga_error():
    wf: Either[str, callable] = Left("func err")
    assert Right(5).apply(wf) == Left("func err")


def test_apply_left_con_right_es_noop():
    wf = Right(lambda x: x + 1)
    assert Left("val err").apply(wf) == Left("val err")



# Monad (bind)                                                          #


def test_bind_sobre_right():
    assert Right(5).bind(lambda x: Right(x * 2)) == Right(10)


def test_bind_sobre_left_es_noop():
    assert Left("err").bind(lambda x: Right(x * 2)) == Left("err")


def test_bind_puede_cambiar_a_left():
    assert Right(5).bind(lambda x: Left("falló")) == Left("falló")



# Leyes de mónada                                                       #


def test_ley_identidad_izquierda():
    """unit(a).bind(f) == f(a)"""
    f = lambda x: Right(x + 1)
    assert Either.unit(5).bind(f) == f(5)


def test_ley_identidad_derecha():
    """m.bind(unit) == m"""
    for m in [Right(5), Left("err")]:
        assert m.bind(Either.unit) == m


def test_ley_asociatividad():
    """m.bind(f).bind(g) == m.bind(lambda x: f(x).bind(g))"""
    f = lambda x: Right(x + 1)
    g = lambda x: Right(x * 10)

    for m in [Right(5), Left("err")]:
        izquierda = m.bind(f).bind(g)
        derecha = m.bind(lambda x: f(x).bind(g))
        assert izquierda == derecha


# Consultas 


def test_get_or_else_sobre_right():
    assert Right(5).get_or_else(0) == 5


def test_get_or_else_sobre_left():
    assert Left("err").get_or_else(0) == 0


def test_is_right_y_is_left():
    assert Right(5).is_right() and not Right(5).is_left()
    assert Left("e").is_left() and not Left("e").is_right()



def test_igualdad_por_valor():
    assert Right(5) == Right(5)
    assert Left("e") == Left("e")
    assert Right(5) != Right(6)
    assert Right(5) != Left(5)


def test_hash_permite_usar_en_set():
    s = {Right(5), Right(5), Left("e")}
    assert len(s) == 2