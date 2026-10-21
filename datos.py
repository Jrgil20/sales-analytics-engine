"""Módulo de persistencia y carga de datos.

Responsabilidad única: Leer y validar los archivos CSV de entrada
sin realizar cálculos ni lógica de presentación.
"""

import csv
from pathlib import Path
from typing import Dict, List, Tuple


def cargar_productos(ruta_archivo: str) -> Dict[str, dict]:
    """Lee el archivo CSV de productos (precios).

    Formato esperado por fila:
        Nombre, Código, Descripción, Precio
    """
    path = Path(ruta_archivo)
    if not path.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de productos en: {ruta_archivo}")

    productos = {}
    with open(path, mode="r", newline="", encoding="utf-8") as csvfile:
        lector = csv.reader(csvfile)
        for num_fila, fila in enumerate(lector, start=1):
            if not fila or not any(campo.strip() for campo in fila):
                continue
            if len(fila) < 4:
                raise ValueError(f"Fila {num_fila} inválida en {path.name}: faltan columnas.")

            nombre, codigo, descripcion, precio_str = fila[0].strip(), fila[1].strip(), fila[2].strip(), fila[3].strip()
            try:
                precio = float(precio_str)
            except ValueError as err:
                raise ValueError(f"Precio inválido '{precio_str}' en fila {num_fila} de {path.name}") from err

            productos[codigo] = {
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
            }

    return productos


def cargar_ventas(ruta_archivo: str) -> Tuple[Dict[str, Dict[str, int]], List[str]]:
    """Lee el archivo CSV de ventas diarias.

    Retorna:
        - ventas: diccionario {codigo_producto: {fecha: cantidad_vendida}}
        - fechas: lista de fechas ordenadas cronológicamente
    """
    path = Path(ruta_archivo)
    if not path.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de ventas en: {ruta_archivo}")

    ventas = {}
    fechas = []

    with open(path, mode="r", newline="", encoding="utf-8") as csvfile:
        lector = csv.DictReader(csvfile)
        if not lector.fieldnames or "fecha" not in lector.fieldnames:
            raise ValueError(f"El archivo {path.name} no contiene la columna 'fecha'.")

        codigos = [c for c in lector.fieldnames if c != "fecha"]
        for codigo in codigos:
            ventas[codigo] = {}

        for num_fila, fila in enumerate(lector, start=2):
            fecha = fila.get("fecha")
            if not fecha:
                continue
            fecha = fecha.strip()
            fechas.append(fecha)

            for codigo in codigos:
                cantidad_str = fila.get(codigo, "0")
                try:
                    cantidad = int(cantidad_str) if cantidad_str else 0
                except ValueError as err:
                    raise ValueError(f"Cantidad inválida en {codigo} el {fecha} (fila {num_fila})") from err
                ventas[codigo][fecha] = cantidad

    return ventas, fechas
