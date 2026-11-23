# Archivos para el reporte

Las rutas siguientes parten de la carpeta `code`. Convertir los CSV en tablas e insertar los PNG como figuras. Este es el orden sugerido de presentación.

| Ruta | Uso en el reporte |
|---|---|
| `resultados_preprocesamiento/distribucion_clases.csv` | Mostrar que hay 20 registros por cada clase. |
| `resultados_preprocesamiento/auditoria_dataset.json` | Describir tamaño, variables y ausencia de faltantes o duplicados; resumirlo en texto. |
| `resultados/comparacion_validacion.csv` | Comparar las tres configuraciones y justificar la selección de la red de 16 neuronas ReLU, época 53. |
| `resultados/curvas_sin_longitud_relu_16.png` | Explicar el aprendizaje y la elección de iteraciones del modelo inicial. |
| `resultados/correlacion_entrenamiento.png` | Mostrar las correlaciones entre características. |
| `resultados/pares_correlacion_alta.csv` | Documentar los pares con correlación absoluta mayor que 0.8. |
| `resultados/caracteristicas_eliminadas.csv` | Presentar las características eliminadas y el motivo. |
| `resultados/caracteristicas_conservadas.csv` | Enumerar las 17 características finales, frente a las 29 iniciales. |
| `resultados/curvas_reducido_relu_16.png` | Comparar el aprendizaje después de reducir características. |
| `resultados/metricas_prueba.csv` | Tabla principal de resultados: accuracy, precisión, recall y F1 de ambas fases. |
| `resultados/comparacion_prueba.png` | Comparación visual del rendimiento inicial y reducido. |
| `resultados/matriz_confusion_sin_longitud.png` | Identificar qué clases confunde el modelo inicial. |
| `resultados/matriz_confusion_reducido.png` | Mostrar cómo cambian los errores tras la reducción. |
| `resultados/reporte_clases_sin_longitud.csv` | Analizar precisión, recall y F1 por clase del modelo inicial. |
| `resultados/reporte_clases_reducido.csv` | Comparar el rendimiento por clase después de reducir variables. |

## Archivos de apoyo y entrega

- `resultados/notas_para_reporte.md`: base para redactar metodología, interpretación y conclusiones.
- `resultados/ejecucion.json`: consultar semilla, particiones, versiones y configuración para describir la metodología.
- `resultados/dataset_reducido.csv`: entregar como archivo aparte, sin pegar sus 200 filas en el reporte.

## Anexos opcionales

Las curvas de las otras configuraciones pueden incluirse en anexos:

- `resultados/curvas_sin_longitud_tanh_32.png`
- `resultados/curvas_sin_longitud_relu_32_16.png`
- `resultados/curvas_reducido_tanh_32.png`
- `resultados/curvas_reducido_relu_32_16.png`

Para explicar la selección de características, usar las correlaciones de `resultados/`, calculadas únicamente con entrenamiento. Las correlaciones de `resultados_preprocesamiento/` son descriptivas del dataset completo.

Las cifras y la configuración indicadas corresponden a la ejecución revisada. Si se vuelve a ejecutar con otros parámetros o datos, comprobarlas contra `resultados/ejecucion.json` y los CSV actualizados.
