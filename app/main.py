"""

Aplicación de ejemplo: pipeline de procesamiento de eventos de e-commerce.

Demuestra el framework completo:
  - Stream (map, filter, reduce, bind)
  - Either (manejo funcional de errores, sin try/except)
  - utils (traverse, collect, catch_each)

Flujo:
  eventos crudos -> parse -> filtrar válidos -> calcular totales -> agregar por región -> reportar inválidos
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from monads import Either, Left, Right
from stream import Stream, utils


# --------------------------------------------------------------------- #
# Modelo de dominio                                                     #
# --------------------------------------------------------------------- #

@dataclass(frozen=True)
class Order:
    order_id: str
    region: str
    price: float
    quantity: int

    @property
    def total(self) -> float:
        return self.price * self.quantity


# --------------------------------------------------------------------- #
# Eventos crudos (lo que "llega" del sistema)                           #
# --------------------------------------------------------------------- #

RAW_EVENTS: list[dict[str, Any]] = [
    {"order_id": "A1", "region": "MX", "price": 100.0, "quantity": 2},
    {"order_id": "A2", "region": "US", "price": 50.0, "quantity": 1},
    {"order_id": "A3", "region": "MX", "price": "caro", "quantity": 1},  # price inválido
    {"order_id": "A4", "region": "US", "price": 20.0, "quantity": 5},
    {"order_id": "A5", "region": "MX", "price": 30.0, "quantity": -1},   # qty inválida
    {"order_id": "A6", "region": "CA", "price": 75.0, "quantity": 2},
    {"order_id": "A7", "region": "US", "price": 10.0, "quantity": 10},
]


# --------------------------------------------------------------------- #
# Paso 1: parsear un evento crudo -> Either[error, Order]               #
# --------------------------------------------------------------------- #

def parse_event(raw: dict[str, Any]) -> Either[str, Order]:
    """Intenta convertir un dict en un Order."""
    try:
        order = Order(
            order_id=str(raw["order_id"]),
            region=str(raw["region"]),
            price=float(raw["price"]),
            quantity=int(raw["quantity"]),
        )
    except (KeyError, ValueError, TypeError) as exc:
        return Left(f"parse error: {exc}")

    if order.price <= 0:
        return Left(f"precio inválido: {order.price}")
    if order.quantity <= 0:
        return Left(f"cantidad inválida: {order.quantity}")

    return Right(order)


# Pipeline funcional                                                    #


def process(raw_events: list[dict[str, Any]]) -> None:
    """Ejecuta el pipeline completo e imprime el reporte."""

    # 1. Stream de eventos 
    events = Stream(raw_events)

    # 2. Parsear cada evento 
    #devuele Either (Right o Left) y lo guarda en parsed
    parsed = events.map(parse_event)

    # 3. Separar éxitos y errores 
    rights, lefts = utils.collect(parsed)
    orders = Stream(rights)

    # 4. Calcular totales por pedido, aplica la lambda a cada pedido
    totals = orders.map(lambda o: (o.region, o.total))

    # 5. Agrupar por región (reduce sobre un dict)
    def acc_by_region(acc: dict[str, float], item: tuple[str, float]) -> dict[str, float]:
        region, total = item
        acc[region] = acc.get(region, 0.0) + total
        return acc

    totals_by_region = utils.reduce(totals, acc_by_region, {})

    # 6. Reporte
    print("=" * 55)
    print("  REPORTE DE VENTAS")
    print("=" * 55)
    print(f"  Eventos recibidos : {len(raw_events)}")
    print(f"  Pedidos válidos   : {len(rights)}")
    print(f"  Pedidos inválidos : {len(lefts)}")
    print("-" * 55)

    print("\n  Totales por región:")
    for region in sorted(totals_by_region):
        print(f"    {region}: ${totals_by_region[region]:.2f}")

    total_global = sum(totals_by_region.values())
    print(f"\n  Total global: ${total_global:.2f}")

    if lefts:
        print("\n  Pedidos descartados (errores):")
        for err in lefts:
            print(f"    - {err}")

    # 7.sequence sobre todos los pedidos
    all_parsed = utils.sequence(parsed)
    print("\n  sequence(parsed):")
    if all_parsed.is_right():
        print(f"    OK -> {all_parsed.value}")
    else:
        print(f"    FALLO -> {all_parsed.error!r}")

    print("=" * 55)


# --------------------------------------------------------------------- #
# Entrypoint                                                            #
# --------------------------------------------------------------------- #

if __name__ == "__main__":
    process(RAW_EVENTS)