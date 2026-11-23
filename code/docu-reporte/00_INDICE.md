# Documentación para preparar el reporte

Material básico de teoría, metodología e interpretación aplicado al proyecto EOG. Las cifras corresponden a la ejecución registrada en `../resultados/ejecucion.json`.

| Archivo | Contenido |
|---|---|
| `01_PROBLEMA_Y_DATOS.md` | EOG, clasificación supervisada, características y clases. |
| `02_PREPROCESAMIENTO_Y_CORRELACION.md` | Exclusión de longitud, z-score y reducción por correlación. |
| `03_MLP_Y_PARAMETROS.md` | Funcionamiento de la red, hiperparámetros y curvas. |
| `04_HOLD_OUT_ESTRATIFICADO.md` | División 60/20/20, procedimiento, justificación y limitaciones. |
| `05_METRICAS.md` | Accuracy, precisión, recall, F1, pérdida y matriz de confusión. |
| `06_GUIA_DE_REDACCION_Y_ANALISIS.md` | Estructura del reporte, resultados y preguntas del profesor. |
| `07_ARCHIVOS_PARA_REPORTE.md` | Figuras y tablas que conviene incluir. |
| `08_JUSTIFICACION_METRICAS_Y_PARAMETROS.md` | Texto breve de justificación aplicado a los resultados. |

En las listas de evidencias, las rutas `resultados/` y `resultados_preprocesamiento/` parten de `code`, un nivel arriba de esta carpeta.

## Fuentes

- `../../ProyectoFinal_InstruccionesMLP.pdf`, pp. 1–3: requisitos y rúbrica.
- `../../EOGSignalClassificationBaseonBlinktoSpeakLanguage.pdf`, pp. 4–7: adquisición, metodología, resultados y clases del artículo.
- `../../DataSet_completo.xlsx`: datos proporcionados.
- `../proyecto_mlp.py`: método implementado.
- `../resultados/` y `../resultados_preprocesamiento/`: evidencias de la ejecución y auditoría.

Los datos del artículo proceden de los PDF proporcionados. Las explicaciones teóricas describen los conceptos empleados en el código; no constituyen citas textuales del artículo. No se aplicó K-Fold. El Word permanece sin modificar y esta documentación sirve de apoyo para preparar el reporte final.
