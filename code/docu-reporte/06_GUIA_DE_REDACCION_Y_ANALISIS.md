# Guía de redacción y análisis

## Estructura sugerida

| Sección | Qué explicar | Material de apoyo |
|---|---|---|
| Introducción y objetivo | Reconocimiento de patrones EOG sin longitud y comparación antes/después de reducir redundancias. | `01_PROBLEMA_Y_DATOS.md` |
| Marco teórico | Clasificación supervisada, MLP, z-score, correlación, hold-out y métricas. | Documentos 01 a 05 |
| Dataset y preprocesamiento | 200 registros, diez clases balanceadas, auditoría, exclusión de longitud y escalado. | Auditoría y distribución de clases |
| Metodología | División 60/20/20, semilla, configuraciones, selección de época y control de información reservada. | `04_HOLD_OUT_ESTRATIFICADO.md` y `resultados/ejecucion.json` |
| Resultados iniciales | Comparación de configuraciones, curvas y métricas con 29 entradas. | Comparación de validación y curva sin longitud |
| Reducción y comparación | Umbral, columnas eliminadas, 17 entradas y resultados con la misma red y época. | Correlación, listas, curva reducida y métricas |
| Discusión | Preguntas del profesor, comparación referencial con el artículo y limitaciones. | Apartado siguiente |
| Conclusiones | Qué ocurrió en esta partición y qué no puede afirmarse. | Métricas y errores por clase |
| Referencias y anexos | PDF proporcionados, evidencia adicional, código y dataset reducido. | Índice y lista de archivos |

## Preguntas del profesor

### 1. ¿Los diez patrones son identificables sin longitud?

El 47.5% de accuracy muestra reconocimiento parcial, pero el desempeño es desigual y no permite afirmar que los diez patrones se distinguen de manera fiable. En prueba, el modelo inicial obtuvo recall de 100% para falta de aire, pero de 0% para sí y agua. Cada clase tiene solo cuatro registros de prueba: estos valores no demuestran capacidad o incapacidad absoluta para reconocerla.

### 2. ¿Cuánto ayudaron o perjudicaron las características originales?

Conservar las 29 características permitidas produjo mejores resultados que conservar las 17 seleccionadas: 47.5% frente a 35% de accuracy. Esto sugiere que las variables descartadas aportaban información útil para esta configuración o que la representación reducida necesita otros ajustes. Ambas variantes excluyen longitud; no se ha medido por separado cuánto cambia la MLP al incluirla.

### 3. ¿Eliminar características correlacionadas mejoró o empeoró la clasificación?

La empeoró en esta ejecución: accuracy cayó 12.5 puntos porcentuales y F1 macro pasó de 0.4311 a 0.3099. Una correlación lineal alta no implica que una entrada sea inútil para una red no lineal. Además, la regla conserva la primera columna correlacionada y no busca la combinación con mejor poder predictivo. La comparación mantiene iguales hiperparámetros; no prueba cuál sería la mejor red posible para cada representación.

### 4. ¿Qué limitaciones del artículo se hicieron evidentes?

El artículo reporta un árbol de decisión con 83.4% de accuracy, 19 características y longitud dominante. La MLP del proyecto excluye longitud y utiliza hold-out; el artículo empleó cinco folds y diez entrenamientos. Es una comparación descriptiva entre protocolos distintos, por lo que la diferencia no puede atribuirse solo al algoritmo o a longitud. **K-Fold pertenece al artículo de referencia, no a nuestra implementación.**

El artículo no enumera la lista exacta de características eliminadas por correlación. Indica que el árbol no utilizó sumas/productos en sus decisiones, pero esto no demuestra que fueran todas descartadas en la selección previa. Debe declararse esa falta de detalle, sin inventar una lista.

### 5. ¿El dataset está bien construido para clasificación?

Es útil como ejercicio: está balanceado, contiene etiquetas y características numéricas y no presenta faltantes ni duplicados. Sin embargo, 200 observaciones son pocas para diez clases. La ausencia de ID de participante impide verificar separación por sujetos, y la adquisición controlada no representa por sí sola el uso real en la población destinataria. La buena estructura de la tabla no garantiza independencia entre registros ni utilidad clínica.

## Texto posible de conclusión

En esta partición hold-out estratificada, la MLP sin longitud reconoció parcialmente los patrones y obtuvo 47.5% de accuracy. La reducción por correlación disminuyó las entradas de 29 a 17 y la accuracy a 35%, manteniendo la configuración seleccionada de 16 neuronas ReLU y 53 épocas. Por tanto, eliminar redundancias lineales no mejoró el desempeño observado. Las diferencias por clase, el tamaño reducido del conjunto de prueba y la ausencia de identificadores de participante limitan la generalización de estas conclusiones.

## Comprobación antes de entregar

- Explicar que la selección de configuración usa validación y que la evaluación final usa prueba.
- Incluir curvas de ambas fases, matriz de correlación, métricas y matrices de confusión.
- Enumerar las eliminaciones propias y distinguirlas de la información incompleta del artículo.
- Comparar las cifras del artículo con las limitaciones del cambio de protocolo.
- Responder las cinco preguntas y justificar los hiperparámetros sin presentarlos como óptimos.
- Adjuntar el dataset reducido y el código, además del reporte PDF solicitado.

Fuentes de los resultados: `resultados/metricas_prueba.csv`, `resultados/comparacion_validacion.csv`, `resultados/reporte_clases_sin_longitud.csv`, `resultados/reporte_clases_reducido.csv` y `resultados/ejecucion.json`. Para la referencia bibliográfica del artículo, consultar los datos impresos en su PDF y su DOI `10.1007/978-3-031-46933-6_27`.
