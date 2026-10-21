#!/usr/bin/env python3
"""Punto de entrada principal del sistema de análisis de ventas.

Responsabilidad: Coordinar la interacción con el usuario (menú en consola),
conectar la carga de datos con los cálculos y gestionar la exportación.
"""

import os
from typing import Dict, List, Optional

import calculos
import datos


def limpiar_pantalla() -> None:
    """Limpia la terminal de forma compatible entre Windows y sistemas Unix (Linux/macOS)."""
    os.system("cls" if os.name == "nt" else "clear")


def generar_texto_informe(
    productos: Dict[str, dict],
    ventas: Dict[str, Dict[str, int]],
    fechas: List[str],
    incluir_equipo: bool = False,
) -> str:
    """Genera el reporte consolidado formateado para pantalla o archivo."""
    # 1. Cálculos de ventas
    trimestre_ventas = calculos.calcular_ventas_trimestrales(ventas, productos)
    total_empresa = sum(trimestre_ventas.values())
    ventas_por_producto = calculos.calcular_ventas_totales_por_producto(ventas, productos)
    ventas_diarias = calculos.calcular_ventas_totales_diarias(ventas, productos, fechas)
    ventas_mensuales = calculos.calcular_ventas_mensuales_totales(ventas_diarias, fechas)
    ventas_mensuales_prod = calculos.calcular_ventas_mensuales_productos(ventas, productos, fechas)

    cod_mas, cant_mas, total_mas = calculos.obtener_producto_destacado(
        ventas, productos, mas_vendido=True
    )
    cod_menos, cant_menos, total_menos = calculos.obtener_producto_destacado(
        ventas, productos, mas_vendido=False
    )
    porcentajes = calculos.calcular_porcentajes_ventas(ventas_por_producto, total_empresa)

    lineas: List[str] = []

    # Total general
    lineas.append(f"Ventas totales de la compañía: ${total_empresa:.2f}\n")

    # Ventas por producto
    for codigo, info in productos.items():
        total_prod = ventas_por_producto.get(codigo, 0.0)
        lineas.append(f"Ventas totales de {info['nombre']}: ${total_prod:.2f}")

    lineas.append("\nVentas totales diarias:")
    for fecha in fechas:
        lineas.append(f"{fecha}: ${ventas_diarias[fecha]:.2f}")

    lineas.append("\nVentas mensuales totales:")
    for mes, total_mes in ventas_mensuales.items():
        lineas.append(f"{mes}: ${total_mes:.2f}")

    lineas.append("\nVentas mensuales por cada producto:")
    for mes, prods_mes in ventas_mensuales_prod.items():
        lineas.append(f"{mes}:")
        for codigo, total_mes_prod in prods_mes.items():
            nombre = productos.get(codigo, {}).get("nombre", "Producto Desconocido")
            lineas.append(f"  {nombre}: ${total_mes_prod:.2f}")

    lineas.append(f"\nProducto más vendido: {productos[cod_mas]['nombre']}")
    lineas.append(f"  Cantidad vendida: {cant_mas}")
    lineas.append(f"  Total vendido: ${total_mas:.2f}\n")

    lineas.append(f"Producto menos vendido: {productos[cod_menos]['nombre']}")
    lineas.append(f"  Cantidad vendida: {cant_menos}")
    lineas.append(f"  Total vendido: ${total_menos:.2f}\n")

    lineas.append("Histograma de porcentajes de ventas por producto en el trimestre:")
    for codigo, porcentaje in porcentajes.items():
        if codigo in productos:
            nombre = productos[codigo]["nombre"]
            barras = "*" * int(porcentaje)
            lineas.append(f"{nombre} ({porcentaje:.2f}%): {barras}")

    if incluir_equipo:
        lineas.append("\n--- Integrantes del Equipo ---")
        lineas.append("Nombre1 - CI: xxxxxxx")
        lineas.append("Nombre2 - CI: xxxxxxx")

    return "\n".join(lineas) + "\n"


def mostrar_menu(archivo_precios: str, archivo_ventas: str) -> None:
    print("\n" + "=" * 45)
    print("    SISTEMA DE ANALÍTICA - FERRETERÍA")
    print("=" * 45)
    print(f"1. Configurar nombres de archivo")
    print(f"   [Precios: {archivo_precios}]")
    print(f"   [Ventas:  {archivo_ventas}]")
    print("2. Procesar datos del archivo")
    print("3. Resultados del archivo (pantalla)")
    print("4. Exportar resultados (archivo)")
    print("0. Salir")
    print("=" * 45)


def main() -> None:
    archivo_precios = "productos_ferreteria_precios.csv"
    archivo_ventas = "productos_ferreteria_ventas.csv"
    archivo_salida = "resultados.txt"

    productos: Optional[Dict[str, dict]] = None
    ventas: Optional[Dict[str, Dict[str, int]]] = None
    fechas: Optional[List[str]] = None

    while True:
        mostrar_menu(archivo_precios, archivo_ventas)
        opcion = input("Ingrese una opción: ").strip()

        if opcion == "1":
            print("\n--- Opción 1: Configuración de archivos ---")
            nuevo_p = input(f"Archivo de precios [{archivo_precios}]: ").strip()
            nuevo_v = input(f"Archivo de ventas [{archivo_ventas}]: ").strip()
            if nuevo_p:
                archivo_precios = nuevo_p
            if nuevo_v:
                archivo_ventas = nuevo_v
            # Al cambiar archivos, reiniciamos datos en memoria
            productos, ventas, fechas = None, None, None
            print("Configuración actualizada.")

        elif opcion == "2":
            print("\n--- Opción 2: Procesar datos ---")
            try:
                productos = datos.cargar_productos(archivo_precios)
                ventas, fechas = datos.cargar_ventas(archivo_ventas)
                print(f"✓ Datos cargados correctamente: {len(productos)} productos y {len(fechas)} días de ventas.")
            except (FileNotFoundError, ValueError) as err:
                print(f"✗ Error al procesar archivos: {err}")

        elif opcion == "3":
            print("\n--- Opción 3: Resultados del análisis ---")
            if productos is None or ventas is None or fechas is None:
                print("⚠ Primero debe procesar los datos con la Opción 2.")
            else:
                informe = generar_texto_informe(productos, ventas, fechas, incluir_equipo=False)
                print(informe)

        elif opcion == "4":
            print("\n--- Opción 4: Exportar resultados ---")
            if productos is None or ventas is None or fechas is None:
                print("⚠ Primero debe procesar los datos con la Opción 2.")
            else:
                destino = input(f"Ruta de destino [{archivo_salida}]: ").strip()
                ruta_final = destino if destino else archivo_salida
                informe_completo = generar_texto_informe(productos, ventas, fechas, incluir_equipo=True)
                with open(ruta_final, mode="w", encoding="utf-8") as f:
                    f.write(informe_completo)
                print(f"✓ Informe exportado con éxito a '{ruta_final}'.")

        elif opcion == "0":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida. Por favor, ingrese un número del menú.")

        if opcion in ("1", "2", "3", "4"):
            salir = input("\n¿Desea salir del programa? (y/n): ").strip().lower()
            if salir == "y":
                print("Saliendo del programa...")
                break


if __name__ == "__main__":
    main()
