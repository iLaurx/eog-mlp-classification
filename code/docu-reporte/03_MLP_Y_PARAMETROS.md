# Red MLP e hiperparámetros

## Funcionamiento básico

Un perceptrón multicapa (MLP) es una red neuronal con una capa de entrada, una o más capas ocultas y una capa de salida. Cada neurona combina entradas mediante pesos y un sesgo, y aplica una función de activación. Las capas ocultas permiten aprender relaciones no lineales.

En este proyecto hay 29 entradas en la fase sin longitud y 17 en la reducida. La salida representa las diez clases; el modelo estima sus probabilidades y predice la de mayor probabilidad.

Durante el entrenamiento se calcula una pérdida que expresa el error de las predicciones. La retropropagación calcula cómo modificar los pesos y Adam realiza las actualizaciones. Los pesos son parámetros aprendidos; el número de neuronas y la tasa de aprendizaje son hiperparámetros establecidos antes de entrenar.

## Configuraciones

| Nombre | Capas ocultas | Activación |
|---|---|---|
| `relu_16` | Una capa de 16 neuronas | ReLU |
| `tanh_32` | Una capa de 32 neuronas | tanh |
| `relu_32_16` | Dos capas, de 32 y 16 neuronas | ReLU |

ReLU devuelve cero para valores negativos y conserva los positivos. tanh transforma valores al intervalo entre −1 y 1. Estas configuraciones exploran capacidades y activaciones diferentes con redes pequeñas. Como cambian varios aspectos entre algunas redes, los resultados no permiten atribuir una diferencia únicamente a la activación.

| Parámetro | Valor y razón de uso |
|---|---|
| Optimizador | Adam, para actualizar pesos con tasas adaptativas. |
| Tasa de aprendizaje inicial | 0.001, una elección inicial moderada para las actualizaciones. |
| Regularización `alpha` | 0.001, penalización L2 de pesos grandes para limitar el sobreajuste. |
| Tamaño de lote | 16, para actualizar con grupos pequeños de ejemplos. |
| Semilla | 42, para repetir la inicialización y las particiones bajo las mismas condiciones. |
| Presupuesto | 600 épocas, para observar la evolución de entrenamiento y validación. |

Estos valores forman una exploración limitada; no fueron optimizados exhaustivamente ni se presentan como óptimos.

## Épocas y curvas

Una época es un recorrido por el conjunto de entrenamiento. En el código, cada llamada a `partial_fit` realiza una época y mantiene el estado del optimizador. Se guardan accuracy y pérdida logarítmica en entrenamiento y validación.

La época se elige por mayor accuracy de validación, con menor pérdida de validación para desempatar. Se conserva una copia del modelo de esa época, aunque las curvas continúen hasta 600. No se aplica parada temprana automática.

El modelo elegido fue `relu_16` en la **época 53**. Alcanzó 47.5% de accuracy de validación y pérdida 1.588; la red de 32–16 empató en accuracy, pero tuvo pérdida 2.678. Cada red reducida se evalúa en la misma época que su pareja original. Para prueba se utiliza únicamente la pareja correspondiente a la configuración ganadora de la fase sin longitud.

## Sobreajuste y subajuste

El sobreajuste ocurre cuando la red aprende particularidades del entrenamiento y no las generaliza. Puede observarse si entrenamiento mejora mientras validación se estanca o empeora. Una pérdida de validación creciente con pérdida de entrenamiento decreciente es una señal útil.

El subajuste ocurre cuando el modelo no logra representar suficientemente las relaciones de los datos y su rendimiento es limitado incluso en entrenamiento. Un resultado bajo por sí solo no distingue todas las causas posibles: también influyen los datos, las características y la optimización.

Evidencias: `resultados/comparacion_validacion.csv` y `resultados/curvas_*.png`.
