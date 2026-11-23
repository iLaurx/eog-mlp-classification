# Resultados y notas para el reporte posterior

Este archivo registra una ejecución real. El Word y el PDF del reporte final siguen pendientes.

## Metodología

Clasificación supervisada de diez clases. Se excluyó Longitud de todos los modelos. Separación estratificada 60/20/20, semilla 42; en el dataset original equivale a 120 filas de entrenamiento, 40 de validación y 40 de prueba. La correlación y los dos StandardScaler se ajustaron únicamente con entrenamiento.

Se probaron tres redes hasta 600 épocas. Adam, alpha=0.001, learning_rate_init=0.001 y batch_size=16 son comunes. Cada época candidata se evaluó en validación. Se seleccionó por accuracy (desempate: menor pérdida de validación) en la fase sin Longitud. La fase reducida reutilizó la configuración y la época de su pareja original. El conjunto de prueba se abrió solo para la pareja ganadora.

Configuración seleccionada: relu_16; época 53. Ver curvas para comprobar si la pérdida de entrenamiento baja mientras validación se estanca. Si se vuelve a ajustar después de observar prueba, se necesitará nueva evaluación independiente.

## Resultados de prueba

| Fase | Accuracy | Precision macro | Recall macro | F1 macro |
|---|---:|---:|---:|---:|
| sin_longitud | 0.475 | 0.439 | 0.475 | 0.431 |
| reducido | 0.350 | 0.391 | 0.350 | 0.310 |

Reducción: 29 a 17 predictores; diferencia de accuracy reducida menos original: -12.5 puntos porcentuales. Cada acierto adicional entre las 40 filas de prueba cambia accuracy en 2.5 puntos. Una sola partición pequeña no demuestra una mejora generalizable.

## Respuestas orientativas a las cinco preguntas

1. **Identificación sin longitud.** Las métricas anteriores cuantifican el reconocimiento en esta partición. La exactitud aleatoria uniforme es 10%; eso es una referencia, no una prueba estadística. Revisar recall por clase y matrices antes de afirmar que los diez patrones son distinguibles; un resultado limitado tampoco demuestra imposibilidad.

2. **Características originales.** Ambas fases excluyen longitud; este experimento compara conservar o quitar redundancias. No mide por separado el efecto de incluir longitud.

3. **Reducción.** En esta prueba la diferencia es -12.5 puntos porcentuales. La selección no supervisada elimina redundancias lineales, pero puede perder combinaciones útiles para una MLP. La dirección del cambio debe interpretarse junto con F1 y errores por clase.

4. **Limitaciones del artículo.** El DT del artículo reporta 83.4% usando longitud, 19 características, validación de cinco folds y diez entrenamientos (pp. 5-7). Aquí cambian algoritmo, variables y protocolo; comparar cifras es descriptivo y no demuestra superioridad causal. El artículo no publica la lista exacta de características eliminadas por correlación. Que el árbol no use sumas/productos no significa que se eliminaran antes.

5. **Calidad del dataset.** Está balanceado (20 registros por clase) y sin faltantes, infinitos, duplicados ni constantes en el archivo original. Sin embargo, 200 registros son pocos y no hay ID de participante: no se puede validar generalización a personas nuevas ni garantizar independencia por sujeto. La adquisición controlada con participantes capaces de reproducir patrones no equivale a validación clínica en la población objetivo.

## Características eliminadas en este proyecto

Longitud se excluye por instrucción del profesor. Después se eliminan, por |r| > 0.8 en entrenamiento y siguiendo el orden del Excel:

- SC_Std_Derecha, redundante con SC_Varianza_Derecha (r=0.9327).
- SC_Std_Izquierda, redundante con SC_Varianza_Izquierda (r=0.9485).
- SC_Std_Horizontales, redundante con SC_Varianza_Horizontales (r=0.8789).
- SC_DifMaxMin_Derecha, redundante con SC_Varianza_Derecha (r=0.8713).
- SC_DifMaxMin_Izquierda, redundante con SC_Varianza_Izquierda (r=0.8649).
- SC_DifMaxMin_Horizontales, redundante con SC_Varianza_Horizontales (r=0.8062).
- SC_Multiplicacion_Media, redundante con SC_Varianza_Horizontales (r=-0.8790).
- SC_Multiplicacion_Varianza, redundante con SC_Varianza_Horizontales (r=0.8831).
- SC_Multiplicacion_Std, redundante con SC_Varianza_Horizontales (r=0.8900).
- SC_Multiplicacion_RMS, redundante con SC_Varianza_Horizontales (r=0.8892).
- SC_Suma_Media, redundante con SC_Media_Izquierda (r=0.8378).
- SC_Suma_Std, redundante con SC_Suma_Varianza (r=0.9440).

Las características retenidas y sus nombres completos están en caracteristicas_conservadas.csv. El dataset reducido conserva unidades originales y Clase; no debe usarse para volver a seleccionar características con toda la muestra.

## Recall por clase en prueba

| Clase | Nombre | Sin Longitud | Reducido |
|---:|---|---:|---:|
| 1 | Sí | 0.00 | 0.00 |
| 2 | No | 0.25 | 0.00 |
| 3 | Quiero dormir | 0.75 | 0.75 |
| 4 | Agua | 0.00 | 0.25 |
| 5 | Baño | 0.75 | 0.25 |
| 6 | Quiero comer | 0.75 | 0.75 |
| 7 | No estoy bien | 0.50 | 0.25 |
| 8 | Falta de aire | 1.00 | 0.75 |
| 9 | Tengo dolor | 0.50 | 0.25 |
| 10 | Peligro | 0.25 | 0.25 |

## Fuentes

- ProyectoFinal_InstruccionesMLP.pdf, pp. 1-3; rubrica.md.
- EOG Signal Classification Based on Blink-to-Speak Language (2024), pp. 4-7: adquisición, características, clasificación y resultados. DOI: 10.1007/978-3-031-46933-6_27.
