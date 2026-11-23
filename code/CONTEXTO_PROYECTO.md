# Contexto del proyecto final

## Estado y alcance

Se revisaron íntegramente los dos PDF proporcionados, la rúbrica y la estructura y los valores del Excel. El artículo está escaneado: se leyeron visualmente sus nueve páginas. El Word `../Portada.docx` debe permanecer intacto por petición del usuario.

Este documento prepara el desarrollo y la interpretación posterior. No contiene resultados MLP ni acredita que el proyecto esté completo. El reporte PDF continúa pendiente; dejar el Word intacto no elimina ese entregable. La interpretación y el análisis crítico valen 20 puntos y requieren resultados reales del código.

## Fuentes locales

- `../ProyectoFinal_InstruccionesMLP.pdf`: requisitos del profesor, tres páginas.
- `../EOGSignalClassificationBaseonBlinktoSpeakLanguage.pdf`: artículo de referencia, nueve páginas.
- `../DataSet_completo.xlsx`: tabla de características suministrada.
- `../rubrica.md`: criterios de evaluación; coincide sustancialmente con el PDF de instrucciones.

## Qué problema se debe resolver

Aunque el título de las instrucciones dice «agrupamiento», las fases especifican clasificación supervisada con una red MLP, etiquetas de clase, accuracy y comparación con un árbol de decisión. Se conservarán las diez clases. No se solicita clustering ni eliminar las clases difíciles.

El objetivo central es investigar si los diez patrones son distinguibles al excluir `Longitud`, y comparar MLP antes y después de eliminar características redundantes por correlación.

## Requisitos por fase

| Fase | Requisito | Página de instrucciones |
|---|---|---:|
| 1. Preprocesamiento | Cargar características numéricas, excluir `Longitud`, estandarizar o normalizar; se recomienda z-score. Mostrar distribuciones o correlaciones iniciales. | 1 |
| 2. Clasificación inicial | Usar validación, probar distintas configuraciones MLP y mostrar curva de aprendizaje para justificar las iteraciones. Calcular métricas de clasificación, especialmente accuracy. | 1–2 |
| 3. Correlación | Calcular matriz de correlación, localizar pares con **valor absoluto de r mayor que 0.8**, eliminar redundancias y estandarizar nuevamente si hace falta. | 2 |
| 4. MLP reducido | Repetir las configuraciones de la fase 2 con **los mismos hiperparámetros**, usando las características reducidas. Mostrar curva de aprendizaje y comparar resultados. | 2 |
| 5. Análisis crítico | Elaborar PDF con metodología, resultados, comparación con el DT del artículo, características eliminadas, gráficas y justificación de hiperparámetros. | 2 |

En la comparación «todas las características» significa todas las permitidas, es decir, sin `Longitud`. Tampoco debe incluirse `Clase` entre las entradas del modelo o en la matriz usada para seleccionar predictores.

El reporte deberá responder:

1. ¿Los diez patrones son identificables sin longitud?
2. ¿Cuánto ayudaron o perjudicaron las características originales?
3. ¿Eliminar características correlacionadas mejoró o empeoró la clasificación?
4. ¿Qué limitaciones del artículo se evidenciaron?
5. ¿El dataset está bien construido para clasificación? Justificar.

## Entregables y rúbrica

La página 3 pide PDF, dataset reducido y ejecutables en Python. La rúbrica menciona además notebook y reporte; conviene incluir script `.py` y notebook `.ipynb`. No exige generar un ejecutable Windows `.exe`.

| Criterio | Puntos |
|---|---:|
| Preprocesamiento: normalización y eliminación de longitud | 15 |
| Aplicación inicial correcta de MLP | 15 |
| Métricas de evaluación | 10 |
| Correlación y selección de características | 10 |
| MLP con características reducidas | 15 |
| Visualizaciones | 10 |
| Interpretación y análisis crítico | 20 |
| Presentación de notebook y reporte | 5 |
| Total | 100 |

## Dataset comprobado

`DataSet_completo.xlsx` tiene una sola hoja, `Sheet1`, con **200 filas y 31 columnas**. La columna objetivo es `Clase`. Hay 30 predictores originales, de los cuales `Longitud` se excluye obligatoriamente: quedan **29 predictores candidatos** antes de la reducción por correlación.

- Diez clases, numeradas de 1 a 10, con 20 filas por clase.
- Todas las columnas son numéricas.
- No se encontraron faltantes, infinitos, filas duplicadas ni columnas constantes.
- Las filas están ordenadas por clase: la partición debe mezclar y estratificar.
- No hay identificador de participante, sesión, fecha ni señales crudas.

Los predictores incluyen media, varianza, desviación estándar, número de picos, distancia entre picos y diferencia máximo–mínimo de los canales derecho, izquierdo y horizontal; longitud; características de productos y sumas de canales. El Excel incluye `SC_Multiplicacion_RMS`, pero no RMS individual por canal: no deben inventarse columnas para reproducir literalmente la descripción general del artículo.

La auditoría descriptiva reproducible se guarda en `resultados_preprocesamiento/`. Sus correlaciones usan las 200 observaciones únicamente para describir la fuente: **no son la selección que debe usarse para evaluar el modelo**. Esa selección se ajustará con entrenamiento, sin observar test. No se exportó un dataset reducido a partir del total durante esta auditoría.

## Significado de las clases

Mapeo explícito de la leyenda de la figura 5 del artículo, página 7:

| Clase | Etiqueta del artículo | Traducción |
|---:|---|---|
| 1 | Yes | Sí |
| 2 | No | No |
| 3 | I want to sleep | Quiero dormir |
| 4 | Water | Agua |
| 5 | Toilet | Baño |
| 6 | I feel like eating | Quiero comer |
| 7 | I'm not OK | No estoy bien |
| 8 | Breathlessness | Falta de aire |
| 9 | I'm in pain | Tengo dolor |
| 10 | Danger | Peligro |

## Qué hizo y qué reportó el artículo

Referencia: María Cristina Padilla-Becerra, Diana Karen Macias-Castro, Ricardo Antonio Salido-Ruiz, Sulema Torres-Ramos e Israel Román-Godínez. *EOG Signal Classification Based on Blink-to-Speak Language*. Springer, 2024, CNIB 2023, IFMBE Proceedings 96, páginas 1–9. DOI impreso: `10.1007/978-3-031-46933-6_27`.

| Aspecto | Dato del artículo | Página |
|---|---|---:|
| Participantes | 20: diez mujeres y diez hombres, de 18 a 50 años, sin impedimentos que dificultaran reproducir los movimientos. | 4 |
| Observaciones | Cada persona realiza diez patrones; total 200 registros. | 4 |
| Adquisición | Natus XLTEK EEG 32, muestreo de 256 Hz, tres canales EOG; entrenamiento guiado por video y ritmo de un conteo por segundo. | 4 |
| Acondicionamiento | Filtro de banda de fase cero de 0.5–30 Hz, ventana Kaiser, atenuación 20 dB. | 5 |
| Picos | Umbral definido como media más 1.75 desviaciones estándar. | 5 |
| Caracterización | Canales individuales y señales de suma/producto; estadísticas, picos, distancias, amplitudes y número de muestras. | 5 |
| Reducción | Probaron umbral de correlación 0.7 y prefirieron 0.8; conservaron 19 características. | 5 |
| Clasificador | Árbol de decisión en MATLAB Classification Learner. | 5 |
| Validación | Cinco folds; el modelo se entrenó diez veces bajo las mismas condiciones. | 6 |
| Accuracy | Promedio de **83.4%**. | 6 |
| Clases con 100% de aciertos | Quiero dormir y peligro. | 6 |
| Clases de menor desempeño | Sí, 53%; baño, 65%. También reporta 81% para no estoy bien y 82.5% para dolor. | 6 |
| Atributo dominante | Longitud, que corresponde al número de muestras de la señal; se utiliza en varias divisiones del árbol. | 6–7 |

El artículo explica que las características efectivamente utilizadas por el árbol corresponden a canales individuales, y que las de suma/producto no fueron utilizadas por el algoritmo para clasificar (página 6).

### Límite de información sobre las características eliminadas

El profesor pide reportar las características eliminadas en el artículo. Sin embargo, el artículo proporcionado **no enumera las 19 características retenidas ni la lista exacta de las eliminadas por correlación**. No se debe inventar esa lista.

Debe distinguirse entre:

- Características descartadas en la selección por correlación, cuya lista exacta no está publicada en el documento.
- Características que el árbol finalmente no utilizó en sus divisiones, como suma/producto según el texto de la página 6.
- Características que nuestro procedimiento elimina, cuya lista sí debe generarse y documentarse.

## Implementación sugerida, sencilla y defendible

Estas son decisiones metodológicas recomendadas, no nuevos requisitos del profesor:

1. Usar pandas, NumPy, matplotlib/seaborn y scikit-learn; `MLPClassifier` evita frameworks innecesarios.
2. Separar datos con estratificación y semilla fija. Usar exactamente las mismas particiones para comparar ambos conjuntos de características.
3. Ajustar escalado y selección únicamente con entrenamiento. Si se usa validación cruzada, ajustar ambos dentro de cada fold mediante pipeline o un ciclo claro.
4. Probar unas pocas configuraciones pequeñas, por ejemplo tres o cuatro. Explicar qué cambia: capas, activación, regularización o tasa de aprendizaje.
5. Seleccionar hiperparámetros e iteraciones con validación; reservar test para evaluación. No elegir la mejor configuración maximizando test.
6. Repetir las mismas configuraciones y presupuesto de iteraciones con el dataset reducido para una comparación consistente.
7. Mostrar pérdida por iteración y, preferiblemente, accuracy de entrenamiento/validación por época para justificar convergencia y cantidad de iteraciones.
8. Generar accuracy, precision/recall/F1 macro, métricas por clase y matrices de confusión. No limitarse al promedio global.
9. Exportar pares correlacionados, matriz, columnas conservadas/eliminadas y tabla comparativa de configuraciones.
10. Exportar el dataset reducido con `Clase`, preferiblemente en unidades originales. El escalado pertenece al modelo; documentar el criterio.
11. No filtrar ni reconstruir señales: la fuente disponible ya es la tabla de características.
12. No usar `Longitud` en ningún MLP de las fases solicitadas.

La comparación con 83.4% es **referencial**: cambian el algoritmo, la exclusión de longitud y posiblemente el protocolo de evaluación. No permite atribuir diferencias exclusivamente a la arquitectura MLP o afirmar superioridad causal.

## Límites y preguntas para interpretar resultados reales

- Solo hay 200 observaciones y 20 por clase; los resultados pueden variar por partición o inicialización, y una red grande puede sobreajustar.
- No hay ID de participante. No se puede verificar generalización a personas nuevas ni hacer validación por personas; no se deben inventar IDs a partir del orden.
- La adquisición fue controlada y los participantes podían reproducir los patrones. No equivale a validación clínica en la población destinataria.
- Longitud captura la duración del registro y facilita la separación de ciertas clases, tal como reconoce el análisis del árbol.
- El contraste entre MLP de 29 características y MLP reducido evalúa redundancia; no aísla el efecto de longitud porque ambos modelos deben excluirla.
- Las confusiones deben analizarse por clase. Una accuracy baja no demuestra imposibilidad absoluta de reconocer los patrones.
- No hay faltantes que imputar ni necesidad de eliminar filas: la limpieza no debe introducir cambios artificiosos.
- Una selección por correlación puede variar entre folds. Debe declararse de qué entrenamiento procede la lista del dataset reducido exportado.

El siguiente paso es ejecutar los experimentos y registrar sus resultados reales. Después se podrá completar el análisis crítico y el reporte, manteniendo por ahora intacto el Word.
