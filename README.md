# Sistema de Análisis de Ventas - Ferretería

Proyecto de **Fundamentos de Programación** enfocado en el procesamiento de datos, modularización, eliminación de estado global y análisis estadístico a partir de archivos CSV.

---

## 🎯 Objetivo Pedagógico y Fundamentos

El objetivo principal de este proyecto es demostrar cómo estructurar un software limpio y mantenible aplicando tres conceptos esenciales de la ingeniería de software:

1. **Separación de Responsabilidades (Single Responsibility Principle)**:
   - La entrada/salida de archivos no debe mezclarse con las operaciones matemáticas.
   - La interfaz de usuario (menú) no debe calcular impuestos, totales ni parsear CSVs.

2. **Funciones Puras (Sin Efectos Secundarios)**:
   - Las funciones del módulo `calculos.py` reciben argumentos y retornan valores nuevos.
   - No usan `print()`, no usan `input()` y no dependen de variables globales. Esto permite testearlas de forma unitaria en milisegundos.

3. **Cero Estado Global**:
   - Se eliminaron las sentencias `global` del código original. Los datos viajan explícitamente a través de los parámetros y retornos de las funciones.

---

## 📂 Estructura del Proyecto

```
Proyecto_FundamentosProgramacion/
├── datos.py                         # Carga, lectura y validación de archivos CSV
├── calculos.py                      # Funciones matemáticas y estadísticas puras
├── main.py                          # Menú interactivo, consola y exportación
├── tests/
│   └── test_calculos.py             # Pruebas unitarias automatizadas (unittest)
├── productos_ferreteria_precios.csv # Catálogo de artículos y precios
├── productos_ferreteria_ventas.csv  # Matriz de transacciones diarias
├── resultados.txt                   # Salida exportada del análisis
├── Woker.py                         # Alias de compatibilidad hacia atrás
└── .gitignore                       # Exclusión de archivos temporales y cachés
```

---

## 🧩 Descripción de Módulos

### 1. `datos.py` (Capa de Acceso a Datos)
Contiene la lógica de lectura y validación de archivos:
- `cargar_productos(ruta)`: Lee el CSV de precios y genera un diccionario indexado por el código del producto.
- `cargar_ventas(ruta)`: Lee el CSV de transacciones diarias con `csv.DictReader` y extrae tanto las cantidades vendidas como la lista de fechas.
- **Manejo defensivo**: Lanza excepciones claras (`FileNotFoundError`, `ValueError`) si faltan columnas o los precios no son números válidos.

### 2. `calculos.py` (Lógica de Negocio)
Contiene las funciones que procesan los datos crudos para obtener métricas:
- `calcular_ventas_trimestrales(...)`: Agrupa las ventas por trimestre del año.
- `calcular_ventas_totales_por_producto(...)`: Facturación acumulada por cada artículo.
- `calcular_ventas_totales_diarias(...)`: Suma diaria de ingresos.
- `calcular_ventas_mensuales_totales(...)`: Facturación agrupada por mes.
- `calcular_ventas_mensuales_productos(...)`: Detalle mensual de cada artículo.
- `obtener_producto_destacado(...)`: Identifica el producto de mayor o menor rotación en unidades.
- `calcular_porcentajes_ventas(...)`: Porcentaje de aporte de cada producto al total de ingresos (base para el histograma).

### 3. `main.py` (Presentación y Orquestación)
- Ofrece el menú interactivo con las 5 opciones clásicas.
- Valida que el usuario procese los datos (Opción 2) antes de intentar ver resultados o exportar.
- Multiplataforma: detecta si corre en Windows (`cls`) o Unix (`clear`).

---

## 🚀 Ejecución

### Requisitos
- **Python 3.8+** (utiliza únicamente la biblioteca estándar).

### Ejecutar el programa
```bash
python3 main.py
```

*(También podés ejecutar `python3 Woker.py`, el cual redirige a `main.py`).*

### Ejecutar las pruebas unitarias
```bash
python3 -m unittest discover -s tests
```

---

## 🛡️ ¿Cómo defender este diseño en una entrega?

Si te preguntan por qué el código está organizado de esta manera:
1. *"Dividimos el programa en tres partes: una que **lee los datos** (`datos.py`), una que **hace las cuentas** (`calculos.py`) y otra que **interactúa con el usuario** (`main.py`)."*
2. *"Hicimos esto para evitar el estado global (`global`), que hacía que el programa original fallara si el usuario elegía una opción del menú antes que otra."*
3. *"Gracias a que las funciones de cálculo no hacen `print()`, pudimos escribir pruebas automáticas con `unittest` que verifican que los resultados numéricos sean 100% exactos."*
