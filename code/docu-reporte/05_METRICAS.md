# Métricas de clasificación

## Accuracy

Accuracy o exactitud es la proporción de predicciones correctas:

$$Accuracy = \frac{\text{predicciones correctas}}{\text{total de predicciones}}$$

Es la métrica principal solicitada para comparar con el artículo. Los valores obtenidos no se fijan manualmente: se calculan a partir de las predicciones sobre datos reservados.

## Precisión, recall y F1 por clase

Para una clase, los verdaderos positivos (TP) son sus registros correctamente identificados; los falsos positivos (FP) son registros de otras clases asignados a ella; los falsos negativos (FN) son registros de esa clase asignados a otras.

$$Precision = \frac{TP}{TP+FP}, \qquad Recall = \frac{TP}{TP+FN}$$

La precisión responde: de lo que se predijo como esta clase, ¿cuánto era correcto? El recall responde: de los registros reales de esta clase, ¿cuántos se reconocieron?

$$F1 = 2\frac{Precision\cdot Recall}{Precision+Recall}$$

F1 combina ambas medidas y penaliza que alguna sea muy baja. El código usa `zero_division=0`: cuando un cociente no está definido por falta de predicciones o soporte, reporta cero según esa convención.

## Promedio macro

Se calcula la métrica para cada clase y se obtiene su promedio simple. Las diez clases pesan lo mismo. F1 macro es el promedio de los diez F1 individuales, no el F1 calculado con precisión macro y recall macro.

Como en prueba hay cuatro ejemplos de cada clase, recall macro coincide con accuracy en esta ejecución. Esa igualdad no se cumple necesariamente en datasets desbalanceados.

## Pérdida logarítmica y matriz de confusión

La pérdida logarítmica considera la probabilidad asignada a la clase verdadera. Menor pérdida es mejor; penaliza especialmente predicciones incorrectas hechas con mucha confianza. Por eso dos modelos con la misma accuracy pueden tener pérdidas distintas. Se usa para las curvas y para desempatar en validación.

La matriz de confusión cruza clases reales en filas y predichas en columnas. La diagonal cuenta aciertos; las otras celdas muestran qué patrones se confunden. Es necesaria para entender errores ocultos tras un promedio global.

## Resultados de prueba

| Variante | Accuracy | Precisión macro | Recall macro | F1 macro |
|---|---:|---:|---:|---:|
| Sin longitud, 29 características | 47.50% | 43.88% | 47.50% | 43.11% |
| Reducida, 17 características | 35.00% | 39.15% | 35.00% | 30.99% |

El modelo inicial acertó 19 de 40 registros y el reducido 14 de 40: una disminución de 12.5 puntos porcentuales. La clasificación aleatoria uniforme entre diez clases tendría una accuracy esperada de 10%; esta referencia no reemplaza una prueba estadística.

Para evitar confusiones, distinguir accuracy de validación, usada para seleccionar, de accuracy de prueba, usada para reportar el rendimiento final. En el modelo inicial ambas coinciden en 47.5%, pero proceden de conjuntos distintos.

Evidencias: `resultados/metricas_prueba.csv`, `resultados/reporte_clases_*.csv` y `resultados/matriz_confusion_*.png`.
