# Preprocesamiento y reducción por correlación

## Exclusión de longitud

Se elimina `Longitud` porque el profesor pide estudiar el reconocimiento sin esa variable dominante. El artículo la identifica como especialmente relevante en el árbol de decisión. Ambas MLP del proyecto la excluyen; la comparación entre ellas mide el efecto de reducir otras características, no el efecto aislado de retirar longitud.

## Estandarización z-score

Las entradas pueden tener escalas muy distintas. La estandarización permite que una característica no domine las actualizaciones de la red solo por tener valores numéricos mayores.

Para cada característica:

$$z = \frac{x - \mu_{entrenamiento}}{\sigma_{entrenamiento}}$$

La media y desviación se calculan únicamente con entrenamiento. Después se aplican esos mismos valores a validación y prueba. El procedimiento se realiza por separado para las entradas originales y las reducidas. Estandarizar no obliga a que validación o prueba tengan media cero ni convierte por sí solo una distribución en normal.

## Correlación de Pearson

Pearson mide la asociación lineal entre dos variables, con valores entre −1 y 1. Valores cercanos a 1 indican variación en el mismo sentido; cercanos a −1, variación en sentidos opuestos. Un valor cercano a cero indica poca asociación lineal, pero puede existir una relación no lineal. Correlación tampoco implica causalidad.

Se consideran redundantes los pares con **|r| > 0.8**, siguiendo el umbral solicitado. El valor absoluto incluye correlaciones positivas y negativas fuertes.

## Procedimiento utilizado

1. Excluir `Longitud` y separar `Clase` de las entradas.
2. Dividir los registros en entrenamiento, validación y prueba.
3. Calcular la correlación con las 120 filas de entrenamiento.
4. Recorrer las columnas en el orden del Excel y conservar una columna cuando no supere el umbral con ninguna ya conservada.
5. Eliminar una columna si supera el umbral con una conservada y registrar esa pareja como motivo.
6. Aplicar las columnas seleccionadas a los tres conjuntos y ajustar el nuevo escalador solo con entrenamiento.

Se conservaron **17 de las 29 características**. El criterio usa las entradas y no las etiquetas para decidir qué conservar. Mantener la primera columna ofrece una regla sencilla y reproducible; no garantiza conservar la variable con mayor utilidad predictiva. Una redundancia lineal puede seguir siendo útil para una MLP, por lo que la reducción no garantiza mejorar la clasificación.

## Fuga de información y exportación

Ajustar el escalado o seleccionar variables con todos los registros permitiría que datos reservados influyeran en el modelo. Por eso se usan solo estadísticas de entrenamiento.

Las correlaciones de `resultados_preprocesamiento/` describen las 200 observaciones; para justificar las eliminaciones del modelo se deben usar las de `resultados/`, ajustadas con entrenamiento. Sus valores y pares pueden diferir.

`resultados/dataset_reducido.csv` contiene las 200 filas, las columnas seleccionadas y `Clase`, en unidades originales. La selección procede de entrenamiento; el archivo exportado no es un conjunto independiente y no se debe volver a seleccionar sobre su totalidad para repetir la evaluación.

Evidencias: `resultados/correlacion_entrenamiento.png`, `resultados/pares_correlacion_alta.csv`, `resultados/caracteristicas_eliminadas.csv` y `resultados/caracteristicas_conservadas.csv`.
