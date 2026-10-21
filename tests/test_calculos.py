"""Pruebas unitarias para el módulo de cálculos y datos."""

import unittest

import calculos
import datos


class TestCalculosFerreteria(unittest.TestCase):
    """Comprueba las funciones puras de cálculos con un dataset controlado."""

    def setUp(self) -> None:
        self.productos = {
            "FB-01": {"nombre": "Martillo", "descripcion": "Martillo acero", "precio": 10.0},
            "EY-10": {"nombre": "Llave", "descripcion": "Llave inglesa", "precio": 5.0},
        }
        self.fechas = ["01/10/23", "02/10/23"]
        self.ventas = {
            "FB-01": {"01/10/23": 2, "02/10/23": 3},  # 5 uds = $50
            "EY-10": {"01/10/23": 10, "02/10/23": 20},  # 30 uds = $150
        }

    def test_calcular_ventas_trimestrales(self) -> None:
        # Octubre pertenece al Trimestre 4: 50 + 150 = 200
        trimestres = calculos.calcular_ventas_trimestrales(self.ventas, self.productos)
        self.assertEqual(trimestres[4], 200.0)

    def test_calcular_ventas_totales_por_producto(self) -> None:
        totales = calculos.calcular_ventas_totales_por_producto(self.ventas, self.productos)
        self.assertEqual(totales["FB-01"], 50.0)
        self.assertEqual(totales["EY-10"], 150.0)

    def test_calcular_ventas_totales_diarias(self) -> None:
        # 01/10/23: 2*10 + 10*5 = 70
        # 02/10/23: 3*10 + 20*5 = 130
        diarias = calculos.calcular_ventas_totales_diarias(self.ventas, self.productos, self.fechas)
        self.assertEqual(diarias["01/10/23"], 70.0)
        self.assertEqual(diarias["02/10/23"], 130.0)

    def test_producto_destacado(self) -> None:
        cod_mas, cant_mas, tot_mas = calculos.obtener_producto_destacado(
            self.ventas, self.productos, mas_vendido=True
        )
        self.assertEqual(cod_mas, "EY-10")
        self.assertEqual(cant_mas, 30)
        self.assertEqual(tot_mas, 150.0)

        cod_menos, cant_menos, tot_menos = calculos.obtener_producto_destacado(
            self.ventas, self.productos, mas_vendido=False
        )
        self.assertEqual(cod_menos, "FB-01")
        self.assertEqual(cant_menos, 5)
        self.assertEqual(tot_menos, 50.0)

    def test_calcular_porcentajes_ventas(self) -> None:
        totales = {"FB-01": 50.0, "EY-10": 150.0}
        porcentajes = calculos.calcular_porcentajes_ventas(totales, 200.0)
        self.assertEqual(porcentajes["FB-01"], 25.0)
        self.assertEqual(porcentajes["EY-10"], 75.0)


class TestIntegracionDatosReales(unittest.TestCase):
    """Comprueba que los datos reales de la ferretería produzcan los valores esperados."""

    def test_dataset_real(self) -> None:
        productos = datos.cargar_productos("productos_ferreteria_precios.csv")
        ventas, fechas = datos.cargar_ventas("productos_ferreteria_ventas.csv")

        trimestres = calculos.calcular_ventas_trimestrales(ventas, productos)
        total_empresa = sum(trimestres.values())
        self.assertAlmostEqual(total_empresa, 69253.78, places=2)

        cod_mas, cant_mas, _ = calculos.obtener_producto_destacado(ventas, productos, mas_vendido=True)
        self.assertEqual(productos[cod_mas]["nombre"], "Llave inglesa")
        self.assertEqual(cant_mas, 296)


if __name__ == "__main__":
    unittest.main()
