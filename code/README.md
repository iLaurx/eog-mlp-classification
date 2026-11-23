# Proyecto final: clasificación EOG con MLP

Implementación en Python de las fases indicadas por el profesor. No modifica el Excel ni los PDF y deja pendiente el Word y el reporte PDF.

## Estado de verificación (23 de noviembre de 2026)

Se verificaron la sintaxis del script y las seis celdas de código del notebook, la lectura real del Excel (200 filas, 29 predictores sin Longitud) y la selección por correlación: toda variable eliminada tiene una pareja conservada por encima del umbral, y ninguna pareja conservada lo supera. Los archivos de `resultados_preprocesamiento` son una auditoría descriptiva; no son resultados de entrenamiento ni la selección final.

**El entrenamiento todavía no se ha ejecutado.** Falta `scikit-learn` y el entorno no pudo resolver `pypi.org` para instalarlo. No se han producido métricas, gráficas de MLP ni el dataset reducido definitivo. Después de instalar las dependencias, ejecutar el script con los comandos siguientes. Los resultados deben revisarse antes de preparar el reporte final.

## Ejecutar en Windows

Desde una terminal situada en esta carpeta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe proyecto_mlp.py
```

El script busca `../DataSet_completo.xlsx` usando su propia ubicación, por lo que también funciona al ejecutarlo desde otra carpeta. Guarda los resultados en `code/resultados`. Se pueden indicar rutas distintas:

```powershell
.\.venv\Scripts\python.exe proyecto_mlp.py --dataset "..\DataSet_completo.xlsx" --salida resultados
```

Para el notebook `proyecto_final.ipynb`, seleccionar el intérprete de `.venv` en VS Code o ejecutar `jupyter lab` con ese entorno. El notebook reutiliza el script: no mantiene una segunda implementación.

## Decisiones del experimento

- Clasificación supervisada de `Clase` (1 a 10); no clustering.
- Se excluye `Longitud` siempre: quedan 29 variables en la primera fase.
- División estratificada con semilla 42: 60% entrenamiento, 20% validación, 20% prueba. Con el archivo original, 12/4/4 registros de cada clase.
- Correlación de Pearson y escalado z-score aprendidos **solo en entrenamiento**. Las medias y escalas quedan exportadas.
- Eliminación de variables con **|r| > 0.8**. Se conserva la primera variable según el orden del Excel; una posterior se elimina si está correlacionada con una ya conservada. No se utilizan las etiquetas para elegir variables.
- Tres redes: `(16,)` ReLU, `(32,)` tanh y `(32,16)` ReLU. Permiten comparar capacidad y activación con un costo pequeño; no constituyen una búsqueda exhaustiva ni aíslan todos los efectos de los hiperparámetros.
- Adam, `alpha=0.001`, `learning_rate_init=0.001`, lotes de 16, sin parada temprana automática. Cada `partial_fit` realiza una época y conserva el estado del optimizador.
- Presupuesto de 600 épocas. Cada configuración original elige su época por la mayor accuracy de validación; los empates se resuelven con menor pérdida de validación. Se guarda una copia real del modelo en esa época.
- La fase reducida repite **la misma configuración y el mismo número de épocas** elegidos para su pareja original. Sus curvas muestran las 600 épocas pero la evaluación corresponde a la época marcada, no necesariamente la última.
- La configuración global se elige solo con validación de la fase original. Únicamente esa pareja de modelos accede a prueba. Esto prioriza una comparación controlada; la MLP reducida podría necesitar otros ajustes, pero realizarlos cambiaría la comparación solicitada.
- No se vuelve a entrenar con validación para mantener la misma selección de columnas, los mismos escaladores y las mismas curvas que sustentan la evaluación.

## Archivos que produce

| Archivo | Contenido |
|---|---|
| `comparacion_validacion.csv` | Las seis combinaciones de fase y configuración, sus épocas y métricas de validación |
| `metricas_prueba.csv` | Accuracy, precision, recall y F1 macro de la pareja seleccionada |
| `reporte_clases_*.csv` | Métricas por clase, con los nombres del artículo |
| `predicciones_prueba.csv`, `particiones.csv` | Predicciones y trazabilidad de filas; fila de Excel incluye encabezado |
| `curvas_*.png` y `.csv` | Pérdida y accuracy de entrenamiento/validación por época |
| `matriz_confusion_*.png` | Errores por clase en prueba |
| `correlacion_entrenamiento.*`, `pares_correlacion_alta.csv` | Matriz y todas las parejas por encima del umbral |
| `caracteristicas_eliminadas.csv`, `caracteristicas_conservadas.csv` | Selección y motivo de cada eliminación |
| `dataset_reducido.csv` | Las 200 filas con columnas seleccionadas y `Clase`, en unidades originales |
| `escalado_*.csv`, `resumen_caracteristicas.csv` | Parámetros z-score de entrenamiento y descripción del dataset |
| `comparacion_prueba.png` | Comparación de accuracy y F1 macro |
| `ejecucion.json` | Semilla, particiones, configuración y versiones de dependencias |
| `notas_para_reporte.md` | Resultados reales y observaciones para desarrollar después el reporte |

El CSV reducido usa el punto como separador decimal y comas entre columnas. La selección se aprende con entrenamiento y luego se aplica a las 200 filas; no es un nuevo conjunto independiente. Para repetir correctamente la evaluación, usar el Excel original con el script y no seleccionar sobre el CSV completo.

## Interpretación y límites

El artículo reporta 83.4% con un árbol de decisión de MATLAB, 19 características que incluyen longitud, validación de cinco folds y diez entrenamientos. Nuestro holdout con MLP sin longitud no reproduce esas condiciones: la comparación es referencial.

El artículo no enumera la lista exacta de características eliminadas por correlación. Que el árbol no use sumas/productos no demuestra que fueran descartados en esa selección. No se inventa esa lista.

Son solo 200 registros y 40 de prueba: cada acierto cambia accuracy en 2.5 puntos porcentuales. No hay identificador de participante y no puede validarse por personas. El balance entre clases y la ausencia de faltantes no garantizan independencia ni uso clínico. Los CSV y matrices permiten analizar las diez clases sin afirmar que una sola partición demuestra generalización.

## Referencias

- `ProyectoFinal_InstruccionesMLP.pdf`, pp. 1–3, y `rubrica.md`.
- *EOG Signal Classification Based on Blink-to-Speak Language*, pp. 4–7. DOI: 10.1007/978-3-031-46933-6_27.

El reporte PDF y la edición del Word son una etapa posterior, fuera del alcance de esta implementación.
