# Diccionario de Datos

Este documento describe la estructura, tipos de datos, restricciones y formato de los archivos fuente utilizados por el sistema.

---

## 1. Catálogo de Precios y Artículos

- **Archivo**: `productos_ferreteria_precios.csv`
- **Formato**: CSV estándar delimitado por comas (`,`), codificación UTF-8.
- **Cabecera**: **No posee fila de cabecera**. Cada fila representa un producto único.

### Estructura de Columnas

| Posición | Campo | Tipo de Dato | Obligatorio | Descripción / Restricciones | Ejemplo |
|:---:|---|---|:---:|---|---|
| 1 | `Nombre` | `String` | Sí | Nombre descriptivo del producto comercial. | `Martillo grande` |
| 2 | `Código` | `String` | Sí | Identificador alfanumérico único (clave primaria). Formato habitual: `XX-00`. | `FB-01` |
| 3 | `Descripción` | `String` | Sí | Detalle técnico del material, medida o uso. | `Martillo mango metálico y cabezal grande de acero` |
| 4 | `Precio` | `Float` | Sí | Valor monetario unitario en dólares. Debe ser mayor o igual a `0.0`. | `30.25` |

### Ejemplo de registros
```csv
Martillo grande ,FB-01,Martillo mango metálico y cabezal grande de acero,30.25
Serrucho,CT-20,Serrucho para corte grueso tamaño grande,15.18
Llave inglesa,EY-10,Llave inglesa de acero inóxidable tamaño mediano,7.93
Taladro percusión,PD-05,Taladro percusión para uso en concreto,80.34
```

---

## 2. Transacciones Diarias de Ventas

- **Archivo**: `productos_ferreteria_ventas.csv`
- **Formato**: CSV estándar delimitado por comas (`,`), codificación UTF-8.
- **Cabecera**: **Posee fila de cabecera obligatoria**. La primera columna es `fecha` y las siguientes coinciden con los códigos del catálogo.

### Estructura de Columnas

| Columna | Tipo de Dato | Obligatorio | Descripción / Restricciones | Ejemplo |
|---|---|:---:|---|---|
| `fecha` | `String` (Fecha) | Sí | Fecha de la jornada en formato `DD/MM/AA`. | `01/10/23` |
| `[CÓDIGO_PRODUCTO]` | `Integer` | Sí | Cantidad entera de unidades vendidas de ese producto en esa fecha (>= 0). | `2` |

### Ejemplo de registros
```csv
fecha,FB-01,CT-20,EY-10,TT-08,PD-05,BR-23,ES-01,GS-03,HW-25,LD-30
01/10/23,2,6,6,4,1,2,0,5,5,4
02/10/23,3,2,0,0,5,4,5,4,5,0
03/10/23,4,4,5,0,4,6,6,0,6,2
```

---

## 3. Reglas de Integridad y Validación

El módulo `datos.py` valida automáticamente las siguientes reglas al procesar los archivos:
1. **Existencia física**: Si el archivo no existe en la ruta dada, emite un error `FileNotFoundError`.
2. **Número de columnas**: En el archivo de precios, cada fila debe poseer exactamente 4 valores; de lo contrario se descarta o alerta con `ValueError`.
3. **Conversión de tipos**:
   - Los precios deben poder convertirse a punto flotante (`float(precio)`).
   - Las cantidades vendidas deben poder convertirse a enteros (`int(cantidad)`).
4. **Correspondencia de códigos**: Las columnas del CSV de ventas deben existir en el diccionario de productos para poder calcular el total facturado.
