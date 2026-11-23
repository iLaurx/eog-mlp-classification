import argparse
from copy import deepcopy
import json
from pathlib import Path
import platform

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.metrics import (accuracy_score, classification_report,
                             ConfusionMatrixDisplay, f1_score, log_loss,
                             precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler


BASE = Path(__file__).resolve().parent
SEMILLA = 42
UMBRAL = 0.8
CLASES = np.arange(1, 11)
NOMBRES = ["Sí", "No", "Quiero dormir", "Agua", "Baño", "Quiero comer",
           "No estoy bien", "Falta de aire", "Tengo dolor", "Peligro"]
CONFIGURACIONES = [
    {"nombre": "relu_16", "hidden_layer_sizes": (16,), "activation": "relu"},
    {"nombre": "tanh_32", "hidden_layer_sizes": (32,), "activation": "tanh"},
    {"nombre": "relu_32_16", "hidden_layer_sizes": (32, 16), "activation": "relu"},
]


def guardar_csv(tabla, ruta, indice=False):
    tabla.to_csv(ruta, index=indice, encoding="utf-8-sig")


def cargar_datos(ruta):
    ruta = Path(ruta)
    datos = (pd.read_csv(ruta) if ruta.suffix.lower() == ".csv"
             else pd.read_excel(ruta, sheet_name="Sheet1"))
    if not {"Longitud", "Clase"}.issubset(datos.columns):
        raise ValueError("El Excel debe incluir las columnas Longitud y Clase.")
    if not all(pd.api.types.is_numeric_dtype(datos[c]) for c in datos.columns):
        raise ValueError("Se esperan únicamente columnas numéricas.")
    if not np.isfinite(datos.to_numpy(dtype=float)).all():
        raise ValueError("Hay valores faltantes o infinitos; revisar el Excel.")
    if set(datos["Clase"].unique()) != set(CLASES):
        raise ValueError("Se esperan las diez clases enteras de 1 a 10.")
    X = datos.drop(columns=["Longitud", "Clase"])
    if X.nunique().min() <= 1:
        raise ValueError("Hay características constantes; revisar antes de escalar.")
    return datos, X, datos["Clase"].astype(int)


def dividir_datos(X, y):
    desarrollo, prueba = train_test_split(
        X.index, test_size=0.2, stratify=y, random_state=SEMILLA)
    entrenamiento, validacion = train_test_split(
        desarrollo, test_size=0.25, stratify=y.loc[desarrollo], random_state=SEMILLA)
    return entrenamiento, validacion, prueba


def seleccionar_caracteristicas(X_entrenamiento):
    correlacion = X_entrenamiento.corr(method="pearson")
    pares = []
    columnas = list(correlacion.columns)
    for i, primera in enumerate(columnas):
        for segunda in columnas[i + 1:]:
            r = float(correlacion.loc[primera, segunda])
            if abs(r) > UMBRAL:
                pares.append({"caracteristica_1": primera, "caracteristica_2": segunda,
                              "r": r, "abs_r": abs(r)})
    conservadas, eliminadas = [], []
    for columna in columnas:
        redundante = next((c for c in conservadas
                           if abs(correlacion.loc[c, columna]) > UMBRAL), None)
        if redundante is None:
            conservadas.append(columna)
        else:
            eliminadas.append({"eliminada": columna, "conservada": redundante,
                               "r": float(correlacion.loc[redundante, columna])})
    return (correlacion, pd.DataFrame(pares, columns=[
        "caracteristica_1", "caracteristica_2", "r", "abs_r"]), conservadas,
        pd.DataFrame(eliminadas, columns=["eliminada", "conservada", "r"]))


def entrenar(configuracion, X_train, y_train, X_val, y_val, epocas,
             epoca_fija=None):
    modelo = MLPClassifier(
        hidden_layer_sizes=configuracion["hidden_layer_sizes"],
        activation=configuracion["activation"], solver="adam", alpha=0.001,
        learning_rate_init=0.001, batch_size=16, shuffle=True,
        random_state=SEMILLA, early_stopping=False, max_iter=1)
    historial, mejor_clave, elegido, epoca_elegida = [], None, None, None
    for epoca in range(1, epocas + 1):
        modelo.partial_fit(X_train, y_train, classes=CLASES)
        prob_train, prob_val = modelo.predict_proba(X_train), modelo.predict_proba(X_val)
        fila = {
            "epoca": epoca,
            "loss_train": log_loss(y_train, prob_train, labels=CLASES),
            "loss_val": log_loss(y_val, prob_val, labels=CLASES),
            "accuracy_train": accuracy_score(y_train, CLASES[prob_train.argmax(axis=1)]),
            "accuracy_val": accuracy_score(y_val, CLASES[prob_val.argmax(axis=1)]),
        }
        historial.append(fila)
        clave = (fila["accuracy_val"], -fila["loss_val"])
        if epoca_fija is None:
            if mejor_clave is None or clave > mejor_clave:
                mejor_clave, elegido, epoca_elegida = clave, deepcopy(modelo), epoca
        elif epoca == epoca_fija:
            elegido, epoca_elegida = deepcopy(modelo), epoca
    return elegido, pd.DataFrame(historial), epoca_elegida


def graficar_curvas(historial, epoca_elegida, titulo, ruta):
    fig, ejes = plt.subplots(1, 2, figsize=(11, 4))
    for eje, metrica, etiqueta in zip(ejes, ["loss", "accuracy"],
                                    ["Pérdida logarítmica", "Accuracy"]):
        eje.plot(historial["epoca"], historial[f"{metrica}_train"], label="Entrenamiento")
        eje.plot(historial["epoca"], historial[f"{metrica}_val"], label="Validación")
        eje.axvline(epoca_elegida, color="black", linestyle="--",
                    label=f"Época usada: {epoca_elegida}")
        eje.set(xlabel="Época", ylabel=etiqueta)
        eje.grid(alpha=0.2)
        eje.legend(fontsize=8)
    ejes[1].set_ylim(0, 1.03)
    fig.suptitle(titulo)
    fig.tight_layout()
    fig.savefig(ruta, dpi=160)
    plt.close(fig)


def graficar_correlacion(correlacion, ruta):
    fig, eje = plt.subplots(figsize=(13, 11))
    imagen = eje.imshow(correlacion, cmap="RdBu_r", vmin=-1, vmax=1)
    etiquetas = [c.removeprefix("SC_") for c in correlacion.columns]
    eje.set_xticks(range(len(etiquetas)), etiquetas, rotation=90, fontsize=7)
    eje.set_yticks(range(len(etiquetas)), etiquetas, fontsize=7)
    eje.set_title("Correlación de Pearson en entrenamiento (sin Longitud)")
    fig.colorbar(imagen, ax=eje, label="r", shrink=0.75)
    fig.tight_layout()
    fig.savefig(ruta, dpi=170)
    plt.close(fig)


def evaluar(modelo, X_test, y_test, fase, salida):
    prediccion = modelo.predict(X_test)
    reporte = classification_report(y_test, prediccion, labels=CLASES,
                                    target_names=NOMBRES, output_dict=True,
                                    zero_division=0)
    guardar_csv(pd.DataFrame(reporte).T, salida / f"reporte_clases_{fase}.csv", True)
    fig, eje = plt.subplots(figsize=(10, 8))
    ConfusionMatrixDisplay.from_predictions(
        y_test, prediccion, labels=CLASES, display_labels=NOMBRES,
        cmap="Blues", colorbar=False, ax=eje, xticks_rotation=55)
    eje.set(title=f"Prueba: {fase.replace('_', ' ')}", xlabel="Clase predicha",
            ylabel="Clase real")
    fig.tight_layout()
    fig.savefig(salida / f"matriz_confusion_{fase}.png", dpi=160)
    plt.close(fig)
    metricas = {"fase": fase, "accuracy": accuracy_score(y_test, prediccion),
                "precision_macro": precision_score(y_test, prediccion, average="macro", zero_division=0),
                "recall_macro": recall_score(y_test, prediccion, average="macro", zero_division=0),
                "f1_macro": f1_score(y_test, prediccion, average="macro", zero_division=0)}
    return metricas, prediccion, reporte


def escribir_notas(salida, resultados, metricas, elegida, conservadas, eliminadas,
                   reportes, epocas):
    original, reducido = metricas.iloc[0], metricas.iloc[1]
    diferencia = 100 * (reducido["accuracy"] - original["accuracy"])
    texto = [
        "# Resultados y notas para el reporte posterior", "",
        "Este archivo registra una ejecución real. El Word y el PDF del reporte final siguen pendientes.", "",
        "## Metodología", "",
        "Clasificación supervisada de diez clases. Se excluyó Longitud de todos los modelos. "
        "Separación estratificada 60/20/20, semilla 42; en el dataset original equivale a "
        "120 filas de entrenamiento, 40 de validación y 40 de prueba. "
        "La correlación y los dos StandardScaler se ajustaron únicamente con entrenamiento.", "",
        f"Se probaron tres redes hasta {epocas} épocas. Adam, alpha=0.001, "
        "learning_rate_init=0.001 y batch_size=16 son comunes. Cada época candidata se evaluó "
        "en validación. Se seleccionó por accuracy (desempate: menor pérdida de validación) "
        "en la fase sin Longitud. La fase reducida reutilizó la configuración y la época "
        "de su pareja original. El conjunto de prueba se abrió solo para la pareja ganadora.", "",
        f"Configuración seleccionada: {elegida['configuracion']}; época {int(elegida['epoca'])}. "
        "Ver curvas para comprobar si la pérdida de entrenamiento baja mientras validación se estanca. "
        "Si se vuelve a ajustar después de observar prueba, se necesitará nueva evaluación independiente.", "",
        "## Resultados de prueba", "",
        "| Fase | Accuracy | Precision macro | Recall macro | F1 macro |",
        "|---|---:|---:|---:|---:|",
    ]
    for _, fila in metricas.iterrows():
        texto.append(f"| {fila['fase']} | {fila['accuracy']:.3f} | {fila['precision_macro']:.3f} | "
                     f"{fila['recall_macro']:.3f} | {fila['f1_macro']:.3f} |")
    texto += ["", f"Reducción: 29 a {len(conservadas)} predictores; "
              f"diferencia de accuracy reducida menos original: {diferencia:+.1f} puntos porcentuales. "
              "Cada acierto adicional entre las 40 filas de prueba cambia accuracy en 2.5 puntos. "
              "Una sola partición pequeña no demuestra una mejora generalizable.", "",
              "## Respuestas orientativas a las cinco preguntas", "",
              "1. **Identificación sin longitud.** Las métricas anteriores cuantifican el reconocimiento "
              "en esta partición. La exactitud aleatoria uniforme es 10%; eso es una referencia, "
              "no una prueba estadística. Revisar recall por clase y matrices antes de afirmar que "
              "los diez patrones son distinguibles; un resultado limitado tampoco demuestra imposibilidad.", "",
              "2. **Características originales.** Ambas fases excluyen longitud; este experimento "
              "compara conservar o quitar redundancias. No mide por separado el efecto de incluir longitud.", "",
              f"3. **Reducción.** En esta prueba la diferencia es {diferencia:+.1f} puntos porcentuales. "
              "La selección no supervisada elimina redundancias lineales, pero puede perder combinaciones "
              "útiles para una MLP. La dirección del cambio debe interpretarse junto con F1 y errores por clase.", "",
              "4. **Limitaciones del artículo.** El DT del artículo reporta 83.4% usando longitud, "
              "19 características, validación de cinco folds y diez entrenamientos (pp. 5-7). "
              "Aquí cambian algoritmo, variables y protocolo; comparar cifras es descriptivo y no demuestra "
              "superioridad causal. El artículo no publica la lista exacta de características eliminadas "
              "por correlación. Que el árbol no use sumas/productos no significa que se eliminaran antes.", "",
              "5. **Calidad del dataset.** Está balanceado (20 registros por clase) y sin faltantes, "
              "infinitos, duplicados ni constantes en el archivo original. Sin embargo, 200 registros "
              "son pocos y no hay ID de participante: no se puede validar generalización a personas "
              "nuevas ni garantizar independencia por sujeto. La adquisición controlada con participantes "
              "capaces de reproducir patrones no equivale a validación clínica en la población objetivo.", "",
              "## Características eliminadas en este proyecto", "",
              "Longitud se excluye por instrucción del profesor. Después se eliminan, por |r| > 0.8 "
              "en entrenamiento y siguiendo el orden del Excel:", ""]
    for _, fila in eliminadas.iterrows():
        texto.append(f"- {fila['eliminada']}, redundante con {fila['conservada']} (r={fila['r']:.4f}).")
    texto += ["", "Las características retenidas y sus nombres completos están en "
              "caracteristicas_conservadas.csv. El dataset reducido conserva unidades originales y "
              "Clase; no debe usarse para volver a seleccionar características con toda la muestra.", "",
              "## Recall por clase en prueba", "",
              "| Clase | Nombre | Sin Longitud | Reducido |", "|---:|---|---:|---:|"]
    for clase, nombre in zip(CLASES, NOMBRES):
        texto.append(f"| {clase} | {nombre} | {reportes[0][nombre]['recall']:.2f} | "
                     f"{reportes[1][nombre]['recall']:.2f} |")
    texto += ["", "## Fuentes", "",
              "- ProyectoFinal_InstruccionesMLP.pdf, pp. 1-3; rubrica.md.",
              "- EOG Signal Classification Based on Blink-to-Speak Language (2024), "
              "pp. 4-7: adquisición, características, clasificación y resultados. "
              "DOI: 10.1007/978-3-031-46933-6_27.", ""]
    (salida / "notas_para_reporte.md").write_text("\n".join(texto), encoding="utf-8")


def ejecutar(dataset=BASE.parent / "DataSet_completo.xlsx", salida=BASE / "resultados", epocas=600):
    if epocas < 1:
        raise ValueError("El número de épocas debe ser positivo.")
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    datos, X, y = cargar_datos(dataset)
    train, val, test = dividir_datos(X, y)
    correlacion, pares, conservadas, eliminadas = seleccionar_caracteristicas(X.loc[train])
    guardar_csv(correlacion, salida / "correlacion_entrenamiento.csv", True)
    guardar_csv(pares, salida / "pares_correlacion_alta.csv")
    guardar_csv(eliminadas, salida / "caracteristicas_eliminadas.csv")
    guardar_csv(pd.DataFrame({"caracteristica": conservadas}), salida / "caracteristicas_conservadas.csv")
    guardar_csv(datos[conservadas + ["Clase"]], salida / "dataset_reducido.csv")
    particiones = pd.DataFrame({"fila_excel": X.index + 2, "Clase": y, "particion": ""})
    for indices, nombre in [(train, "entrenamiento"), (val, "validacion"), (test, "prueba")]:
        particiones.loc[indices, "particion"] = nombre
    guardar_csv(particiones, salida / "particiones.csv")
    graficar_correlacion(correlacion, salida / "correlacion_entrenamiento.png")
    guardar_csv(X.describe().T, salida / "resumen_caracteristicas.csv", True)

    resultados, modelos, escaladores = [], {}, {}
    for fase, columnas in [("sin_longitud", list(X.columns)), ("reducido", conservadas)]:
        escalador = StandardScaler().fit(X.loc[train, columnas])
        escaladores[fase] = escalador
        X_train = escalador.transform(X.loc[train, columnas])
        X_val = escalador.transform(X.loc[val, columnas])
        guardar_csv(pd.DataFrame({"caracteristica": columnas, "media_train": escalador.mean_,
                                  "escala_train": escalador.scale_}), salida / f"escalado_{fase}.csv")
        for configuracion in CONFIGURACIONES:
            nombre = configuracion["nombre"]
            epoca_fija = None if fase == "sin_longitud" else modelos[("sin_longitud", nombre)][1]
            modelo, historial, epoca = entrenar(
                configuracion, X_train, y.loc[train], X_val, y.loc[val], epocas, epoca_fija)
            modelos[(fase, nombre)] = (modelo, epoca)
            fila = historial.iloc[epoca - 1]
            resultados.append({"fase": fase, "configuracion": nombre, "capas": str(configuracion["hidden_layer_sizes"]),
                               "activacion": configuracion["activation"], "n_caracteristicas": len(columnas),
                               "epoca": epoca, "accuracy_train": fila["accuracy_train"],
                               "accuracy_val": fila["accuracy_val"], "loss_val": fila["loss_val"]})
            guardar_csv(historial, salida / f"curvas_{fase}_{nombre}.csv")
            graficar_curvas(historial, epoca, f"{fase.replace('_', ' ')} / {nombre}",
                            salida / f"curvas_{fase}_{nombre}.png")
            print(f"{fase:14s} {nombre:12s} época={epoca:3d} accuracy_val={fila['accuracy_val']:.3f}")

    resultados = pd.DataFrame(resultados)
    guardar_csv(resultados, salida / "comparacion_validacion.csv")
    elegida = resultados[resultados["fase"] == "sin_longitud"].sort_values(
        ["accuracy_val", "loss_val"], ascending=[False, True], kind="stable").iloc[0]
    metricas, reportes = [], []
    predicciones = pd.DataFrame({"fila_excel": test + 2, "Clase_real": y.loc[test].to_numpy()})
    for fase, columnas in [("sin_longitud", list(X.columns)), ("reducido", conservadas)]:
        modelo, _ = modelos[(fase, elegida["configuracion"])]
        X_test = escaladores[fase].transform(X.loc[test, columnas])
        metrica, prediccion, reporte = evaluar(modelo, X_test, y.loc[test], fase, salida)
        metricas.append(metrica)
        reportes.append(reporte)
        predicciones[f"prediccion_{fase}"] = prediccion
    metricas = pd.DataFrame(metricas)
    guardar_csv(metricas, salida / "metricas_prueba.csv")
    guardar_csv(predicciones, salida / "predicciones_prueba.csv")
    fig, eje = plt.subplots(figsize=(7, 4))
    metricas.set_index("fase")[["accuracy", "f1_macro"]].plot.bar(ax=eje, rot=0)
    eje.set(ylabel="Puntuación en prueba", ylim=(0, 1), xlabel="",
            title=f"Misma configuración: {elegida['configuracion']} ({int(elegida['epoca'])} épocas)")
    eje.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    fig.savefig(salida / "comparacion_prueba.png", dpi=160)
    plt.close(fig)
    metadata = {"dataset": Path(dataset).name, "filas": len(datos), "semilla": SEMILLA,
                "umbral_correlacion": UMBRAL, "presupuesto_epocas": epocas,
                "seleccionada": elegida["configuracion"], "epoca_usada": int(elegida["epoca"]),
                "n_entrenamiento": len(train), "n_validacion": len(val), "n_prueba": len(test),
                "python": platform.python_version(), "numpy": np.__version__,
                "pandas": pd.__version__, "sklearn": sklearn.__version__,
                "configuraciones": CONFIGURACIONES}
    (salida / "ejecucion.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    escribir_notas(salida, resultados, metricas, elegida, conservadas, eliminadas, reportes, epocas)
    print("\nConfiguración elegida solo por validación:", elegida["configuracion"])
    print(metricas.to_string(index=False))
    print("\nArchivos guardados en:", salida.resolve())
    return resultados, metricas


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clasificacion de senales EOG con MLP")
    parser.add_argument("--dataset", type=Path, default=BASE.parent / "DataSet_completo.xlsx")
    parser.add_argument("--salida", type=Path, default=BASE / "resultados")
    parser.add_argument("--epocas", type=int, default=600)
    argumentos = parser.parse_args()
    ejecutar(argumentos.dataset, argumentos.salida, argumentos.epocas)
