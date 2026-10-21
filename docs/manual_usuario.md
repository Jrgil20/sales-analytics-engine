# Manual de Usuario

Guía práctica para la ejecución, navegación y resolución de problemas del Sistema de Análisis de Ventas.

---

## 1. Requisitos Previos

- Tener instalado **Python 3.8 o superior**.
- Contar con los archivos CSV en el mismo directorio del programa:
  - `productos_ferreteria_precios.csv`
  - `productos_ferreteria_ventas.csv`

---

## 2. Cómo Iniciar el Programa

Abrí una terminal en la carpeta del proyecto y ejecutá:

```bash
python3 main.py
```

Aparecerá el menú principal interactivo:

```text
=============================================
    SISTEMA DE ANALÍTICA - FERRETERÍA
=============================================
1. Configurar nombres de archivo
   [Precios: productos_ferreteria_precios.csv]
   [Ventas:  productos_ferreteria_ventas.csv]
2. Procesar datos del archivo
3. Resultados del archivo (pantalla)
4. Exportar resultados (archivo)
0. Salir
=============================================
Ingrese una opción: 
```

---

## 3. Guía de Opciones del Menú

### Opción 1: Configurar nombres de archivo
Permite cambiar las rutas predeterminadas de los archivos de entrada. Útil si querés analizar datos de otro mes o sucursal.
- Si presionás `Enter` sin escribir nada, conserva el nombre actual.
- **Importante**: Al cambiar los archivos, la memoria se reinicia para obligar a procesar los nuevos datos con la Opción 2.

### Opción 2: Procesar datos del archivo
Lee y valida los archivos CSV cargándolos en memoria.
- Si todo es correcto, verás: `✓ Datos cargados correctamente: 10 productos y 92 días de ventas.`
- Si los archivos no existen o tienen errores de formato, el sistema mostrará un mensaje descriptivo sin cerrarse inesperadamente.

### Opción 3: Resultados del archivo (pantalla)
Calcula y muestra en consola el informe completo:
- Facturación total de la compañía.
- Ventas totales por cada producto.
- Detalle diario cronológico.
- Consolidado mensual y desglose por producto.
- Producto estrella (más vendido) y producto de menor rotación.
- Histograma de barras con asteriscos (`*`) representando la cuota de ventas.

### Opción 4: Exportar resultados (archivo)
Genera el archivo `resultados.txt` (o el nombre que elijas) con el mismo contenido visto en pantalla, agregando además la sección de integrantes del equipo al pie del documento.

### Opción 0: Salir
Cierra la aplicación de forma segura.

---

## 4. Preguntas Frecuentes y Solución de Problemas

### "¿Por qué me sale '⚠ Primero debe procesar los datos con la Opción 2'?"
Ocurre si intentás ver resultados (Opción 3) o exportar (Opción 4) sin haber ejecutado antes la Opción 2. Simplemente seleccioná la opción 2 para procesar los datos y luego continuá.

### "¿Cómo cambio los integrantes que salen en el archivo exportado?"
Abrí [`main.py`](../main.py) y en la función `generar_texto_informe`, editá las líneas finales de la sección `incluir_equipo`:
```python
lineas.append("TuNombre - CI: 1234567")
lineas.append("Compañero - CI: 7654321")
```

### "¿Cómo ejecuto las pruebas automáticas?"
En la terminal, ejecutá:
```bash
python3 -m unittest discover -s tests
```
Verás un mensaje confirmando que todas las pruebas pasaron (`OK`).
