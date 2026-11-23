# Validación mediante hold-out estratificado

## Qué método se utilizó

Se utilizó **hold-out estratificado con tres conjuntos**: entrenamiento, validación y prueba. Se hace una división fija de los registros y cada conjunto mantiene la misma función durante todo el experimento. Es un procedimiento básico y común de evaluación supervisada.

La estratificación mantiene las proporciones de las clases en cada conjunto. Aquí evita perder el balance de las diez clases, especialmente porque el Excel está ordenado por etiqueta.

| Conjunto | Porcentaje | Registros totales | Registros por clase | Función |
|---|---:|---:|---:|---|
| Entrenamiento | 60% | 120 | 12 | Ajustar pesos, correlación y escaladores. |
| Validación | 20% | 40 | 4 | Elegir configuración y época de entrenamiento. |
| Prueba | 20% | 40 | 4 | Medir el rendimiento final de la pareja elegida. |

## Cómo se implementó

Primero, `train_test_split` reserva 20% del total para prueba y deja 80% para desarrollo. Después reserva 25% del conjunto de desarrollo para validación: 25% de 80% equivale a 20% del total. El 60% restante se utiliza para entrenar.

Ambas llamadas emplean `stratify` y `random_state=42`. La semilla permite reproducir la división; no fue elegida por obtener una accuracy mayor. `resultados/particiones.csv` identifica las filas asignadas a cada conjunto.

Las mismas particiones se reutilizan para las MLP sin longitud y reducida. No hay rotación de conjuntos ni promedio de evaluaciones entre particiones: **no se utilizó K-Fold ni validación cruzada**. Evaluar cada época sobre las mismas 40 filas de validación no convierte el método en K-Fold.

## Por qué se eligió

Permite distinguir de forma sencilla el ajuste del modelo, la selección de hiperparámetros y la evaluación final. Respeta la restricción de no usar K-Fold y mantiene una comparación con las mismas observaciones entre las dos fases. La división 60/20/20 conserva datos para las tres funciones; no se afirma que sea la única ni la mejor proporción posible.

El conjunto de prueba no decide neuronas, activación o época. Se evalúan en prueba las dos variantes de la configuración seleccionada con validación, manteniendo sus hiperparámetros comparables.

## Limitaciones

- Con 40 observaciones de prueba, cada acierto cambia la accuracy en 2.5 puntos porcentuales.
- Cada clase tiene solo cuatro ejemplos de prueba; su recall cambia en saltos de 25 puntos porcentuales.
- El resultado depende de la partición y la inicialización. Una sola ejecución no mide esa variabilidad ni demuestra significancia estadística.
- Consultar repetidamente la misma validación para elegir épocas y configuraciones también puede adaptar la selección a ese conjunto; por eso se mantiene una prueba separada.
- La estratificación conserva proporciones de etiquetas, pero no garantiza independencia entre participantes. El Excel carece de identificadores para separar por personas.

## Texto breve para el reporte

Se aplicó un esquema hold-out estratificado, dividiendo los 200 registros en 60% para entrenamiento, 20% para validación y 20% para prueba. Se utilizó la semilla 42 para reproducir las particiones y se mantuvo la proporción de las diez clases en cada conjunto. Los pesos, el escalado y la selección por correlación se ajustaron únicamente con entrenamiento. La validación permitió seleccionar la configuración y la época, mientras que la prueba se reservó para comparar el rendimiento final de las variantes sin longitud y reducida. Se utilizaron las mismas filas en ambas fases y no se aplicó K-Fold. Debido al tamaño reducido de prueba, los resultados se interpretan como evidencia de esta partición y no como una estimación definitiva de generalización.
