"""Módulo de cálculos y lógica de negocio.

Responsabilidad única: Procesar los datos matemáticamente mediante
FUNCIONES PURAS (reciben parámetros y retornan resultados, sin hacer print ni I/O).
"""

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple


def calcular_ventas_trimestrales(
    ventas: Dict[str, Dict[str, int]], productos: Dict[str, dict]
) -> Dict[int, float]:
    """Calcula las ventas acumuladas por cada trimestre del año."""
    trimestre_ventas = defaultdict(float)
    for codigo, ventas_producto in ventas.items():
        precio = productos[codigo]["precio"]
        for fecha, cantidad in ventas_producto.items():
            mes = datetime.strptime(fecha, "%d/%m/%y").month
            trimestre = (mes - 1) // 3 + 1
            trimestre_ventas[trimestre] += cantidad * precio
    return dict(trimestre_ventas)


def calcular_ventas_totales_por_producto(
    ventas: Dict[str, Dict[str, int]], productos: Dict[str, dict]
) -> Dict[str, float]:
    """Calcula el total de dinero generado por cada producto."""
    totales = {}
    for codigo, info in productos.items():
        cantidad_total = sum(ventas.get(codigo, {}).values())
        totales[codigo] = cantidad_total * info["precio"]
    return totales


def calcular_ventas_totales_diarias(
    ventas: Dict[str, Dict[str, int]], productos: Dict[str, dict], fechas: List[str]
) -> Dict[str, float]:
    """Calcula el total facturado en cada día registrado."""
    ventas_diarias = defaultdict(float)
    for fecha in fechas:
        for codigo, fechas_dict in ventas.items():
            if fecha in fechas_dict:
                ventas_diarias[fecha] += fechas_dict[fecha] * productos[codigo]["precio"]
    return dict(ventas_diarias)


def calcular_ventas_mensuales_totales(
    ventas_diarias: Dict[str, float], fechas: List[str]
) -> Dict[str, float]:
    """Calcula el total facturado en cada mes manteniendo el orden cronológico."""
    ventas_mensuales = defaultdict(float)
    for fecha in fechas:
        mes = datetime.strptime(fecha, "%d/%m/%y").strftime("%B")
        ventas_mensuales[mes] += ventas_diarias.get(fecha, 0.0)
    return dict(ventas_mensuales)


def calcular_ventas_mensuales_productos(
    ventas: Dict[str, Dict[str, int]], productos: Dict[str, dict], fechas: List[str]
) -> Dict[str, Dict[str, float]]:
    """Calcula la facturación mensual detallada por cada producto."""
    ventas_mensuales = defaultdict(lambda: defaultdict(float))
    for fecha in fechas:
        mes = datetime.strptime(fecha, "%d/%m/%y").strftime("%B")
        for codigo, ventas_producto in ventas.items():
            if fecha in ventas_producto:
                cantidad = ventas_producto[fecha]
                ventas_mensuales[mes][codigo] += cantidad * productos[codigo]["precio"]

    return {mes: dict(prod_dict) for mes, prod_dict in ventas_mensuales.items()}


def obtener_producto_destacado(
    ventas: Dict[str, Dict[str, int]], productos: Dict[str, dict], mas_vendido: bool = True
) -> Tuple[str, int, float]:
    """Devuelve (codigo, cantidad_total, importe_total) del producto más o menos vendido."""
    criterio = max if mas_vendido else min
    codigo = criterio(ventas, key=lambda cod: sum(ventas[cod].values()))
    cantidad = sum(ventas[codigo].values())
    total_dinero = cantidad * productos[codigo]["precio"]
    return codigo, cantidad, total_dinero


def calcular_porcentajes_ventas(
    ventas_por_producto: Dict[str, float], total_ventas: float
) -> Dict[str, float]:
    """Calcula la participación porcentual de cada producto en las ventas globales."""
    if total_ventas <= 0:
        return {codigo: 0.0 for codigo in ventas_por_producto}
    return {
        codigo: (monto / total_ventas) * 100 for codigo, monto in ventas_por_producto.items()
    }
