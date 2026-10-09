"""
Paquete stream: mónada de flujo de datos + utilidades funcionales.

Expone:
    Stream - clase principal (Functor + Applicative + Monad)
    utils  - librería de funciones (map, filter, reduce, catch, ...)
"""
from stream.core import Stream
from stream import utils

__all__ = ["Stream", "utils"]