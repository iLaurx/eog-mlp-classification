# Problema y datos

## EOG y Blink-to-Speak

La electrooculografía (EOG) registra cambios de potencial eléctrico asociados con los movimientos de los ojos. El lenguaje Blink-to-Speak utiliza patrones de movimientos oculares para representar mensajes. El objetivo del proyecto es reconocer diez patrones a partir de características numéricas de sus señales.

Se trabaja con **clasificación supervisada**: cada registro tiene una etiqueta conocida, `Clase`, y la red aprende la relación entre sus características y esa etiqueta. Aunque las instrucciones usan la palabra agrupamiento en el título, el procedimiento implementado es clasificación con MLP.

## Registros, características y objetivo

Un registro es una observación del dataset; una característica es una medición numérica que describe esa observación. Las entradas del modelo se representan mediante X y las etiquetas mediante y.

El Excel tiene 200 registros y 31 columnas: 30 características originales y `Clase`. Al excluir `Longitud`, quedan 29 entradas. `Clase` es únicamente el objetivo y nunca una entrada del modelo.

Las características incluyen media, varianza, desviación estándar, número de picos, distancia entre picos y diferencia máximo–mínimo para distintos canales, además de medidas de sumas y productos. Estas mediciones resumen señales que ya fueron procesadas; el proyecto no recibe señales crudas ni vuelve a filtrarlas.

| Concepto | Significado básico |
|---|---|
| Media | Nivel promedio de los valores de una señal. |
| Varianza y desviación estándar | Dispersión respecto de la media. |
| Número de picos | Cantidad de máximos detectados según el procesamiento original. |
| Distancia entre picos | Separación entre los picos detectados. |
| Diferencia máximo–mínimo | Rango de amplitud. |
| RMS | Raíz del promedio de los valores al cuadrado; resume la magnitud de la señal. |
| Longitud | Número de muestras del registro, asociado con su duración. |

El Excel contiene RMS del producto de canales; no incluye una columna RMS individual para cada canal.

## Clases

| Clase | Mensaje |
|---:|---|
| 1 | Sí |
| 2 | No |
| 3 | Quiero dormir |
| 4 | Agua |
| 5 | Baño |
| 6 | Quiero comer |
| 7 | No estoy bien |
| 8 | Falta de aire |
| 9 | Tengo dolor |
| 10 | Peligro |

Cada clase tiene 20 registros. El mapeo procede de la figura 5, p. 7 del artículo. La auditoría no encontró faltantes, infinitos, duplicados ni columnas constantes. El dataset no contiene identificadores de participante, por lo que no se puede comprobar la generalización a personas nuevas.

Evidencias: `resultados_preprocesamiento/auditoria_dataset.json` y `resultados_preprocesamiento/distribucion_clases.csv`.
