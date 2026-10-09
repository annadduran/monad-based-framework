"""Smoke test de la aplicación de ejemplo."""
from app.main import parse_event, process, RAW_EVENTS
from monads import Left, Right


def test_parse_event_valido():
    raw = {"order_id": "X", "region": "MX", "price": 10.0, "quantity": 2}
    result = parse_event(raw)
    assert result.is_right()
    assert result.value.total == 20.0


def test_parse_event_precio_invalido():
    raw = {"order_id": "X", "region": "MX", "price": "caro", "quantity": 2}
    assert parse_event(raw).is_left()


def test_parse_event_cantidad_negativa():
    raw = {"order_id": "X", "region": "MX", "price": 10.0, "quantity": -1}
    assert parse_event(raw).is_left()


def test_parse_event_falta_campo():
    raw = {"order_id": "X", "region": "MX"}
    assert parse_event(raw).is_left()


def test_process_corre_sin_excepciones(capsys):
    process(RAW_EVENTS)
    out = capsys.readouterr().out
    assert "REPORTE DE VENTAS" in out
    assert "Total global" in out