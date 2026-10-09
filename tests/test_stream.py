"""Tests de la mónada Stream: leyes, functor, applicative y utilidades."""
from stream import Stream


# --------------------------------------------------------------------- #
# Constructores                                                         #
# --------------------------------------------------------------------- #

def test_unit_crea_stream_de_un_elemento():
    assert Stream.unit(5) == Stream.of(5)


def test_of_con_multiples_valores():
    assert Stream.of(1, 2, 3).to_list() == [1, 2, 3]


def test_empty():
    assert Stream.empty().to_list() == []


def test_desde_iterable():
    assert Stream(range(3)).to_list() == [0, 1, 2]


# --------------------------------------------------------------------- #
# Functor (map)                                                         #
# --------------------------------------------------------------------- #

def test_map_aplica_funcion():
    assert Stream.of(1, 2, 3).map(lambda x: x * 2) == Stream.of(2, 4, 6)


def test_map_stream_vacio():
    assert Stream.empty().map(lambda x: x * 2) == Stream.empty()


# --------------------------------------------------------------------- #
# Applicative (apply)                                                   #
# --------------------------------------------------------------------- #

def test_apply_aplica_cada_funcion_a_cada_valor():
    funcs = Stream.of(lambda x: x + 1, lambda x: x * 2)
    values = Stream.of(10, 20)
    assert values.apply(funcs) == Stream.of(11, 21, 20, 40)


# --------------------------------------------------------------------- #
# Monad (bind)                                                          #
# --------------------------------------------------------------------- #

def test_bind_aplana():
    result = Stream.of(1, 2, 3).bind(lambda x: Stream.of(x, -x))
    assert result == Stream.of(1, -1, 2, -2, 3, -3)


def test_bind_puede_descartar_elementos():
    result = Stream.of(1, 2, 3, 4).bind(
        lambda x: Stream.of(x) if x % 2 == 0 else Stream.empty()
    )
    assert result == Stream.of(2, 4)


# --------------------------------------------------------------------- #
# Leyes de mónada                                                       #
# --------------------------------------------------------------------- #

def test_ley_identidad_izquierda():
    f = lambda x: Stream.of(x, x * 10)
    assert Stream.unit(5).bind(f) == f(5)


def test_ley_identidad_derecha():
    s = Stream.of(1, 2, 3)
    assert s.bind(Stream.unit) == s


def test_ley_asociatividad():
    f = lambda x: Stream.of(x + 1)
    g = lambda x: Stream.of(x * 10)
    s = Stream.of(1, 2, 3)

    izquierda = s.bind(f).bind(g)
    derecha = s.bind(lambda x: f(x).bind(g))
    assert izquierda == derecha


# --------------------------------------------------------------------- #
# Utilidades                                                            #
# --------------------------------------------------------------------- #

def test_filter():
    assert Stream.of(1, 2, 3, 4).filter(lambda x: x % 2 == 0) == Stream.of(2, 4)


def test_reduce():
    assert Stream.of(1, 2, 3, 4).reduce(lambda a, b: a + b, 0) == 10


def test_reduce_con_init_no_cero():
    assert Stream.of(1, 2, 3).reduce(lambda a, b: a * b, 10) == 60


def test_take():
    assert Stream.of(1, 2, 3, 4, 5).take(3) == Stream.of(1, 2, 3)


def test_take_mas_de_lo_que_hay():
    assert Stream.of(1, 2).take(10) == Stream.of(1, 2)


def test_drop():
    assert Stream.of(1, 2, 3, 4, 5).drop(2) == Stream.of(3, 4, 5)


# --------------------------------------------------------------------- #
# Protocolo de Python                                                   #
# --------------------------------------------------------------------- #

def test_iteracion():
    assert list(Stream.of(1, 2, 3)) == [1, 2, 3]


def test_len():
    assert len(Stream.of(1, 2, 3)) == 3
    assert len(Stream.empty()) == 0


def test_igualdad_por_valor():
    assert Stream.of(1, 2, 3) == Stream.of(1, 2, 3)
    assert Stream.of(1, 2, 3) != Stream.of(1, 2)


def test_hash_permite_uso_en_set():
    s = {Stream.of(1, 2), Stream.of(1, 2), Stream.of(3)}
    assert len(s) == 2


def test_repr():
    assert repr(Stream.of(1, 2)) == "Stream([1, 2])"


# --------------------------------------------------------------------- #
# Encadenamiento                                                        #
# --------------------------------------------------------------------- #

def test_chaining_completo():
    result = (
        Stream.of(1, 2, 3, 4, 5, 6)
        .filter(lambda x: x % 2 == 0)     # 2, 4, 6
        .map(lambda x: x * 10)            # 20, 40, 60
        .bind(lambda x: Stream.of(x, x + 1))  # 20,21,40,41,60,61
    )
    assert result == Stream.of(20, 21, 40, 41, 60, 61)