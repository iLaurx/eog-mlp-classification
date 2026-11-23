# Clasificación EOG con MLP

Proyecto de Aprendizaje Máquina para clasificar diez patrones oculares. Compara una red MLP sin la variable `Longitud` con otra que utiliza características reducidas por correlación.

## Instalación

Necesitas Python y Git. En una terminal de PowerShell ejecuta:

```powershell
git clone https://github.com/iLaurx/eog-mlp-classification.git
cd eog-mlp-classification
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r code/requirements.txt
```

Si ya descargaste el proyecto, abre la terminal en su carpeta y comienza desde `python -m venv .venv`.

## Ejecución

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe code/proyecto_mlp.py
```

El programa lee `DataSet_completo.xlsx`, entrena los modelos y guarda las métricas, gráficas y el dataset reducido en `code/resultados/`. Al ejecutarlo de nuevo se actualizan esos archivos.

## Notebook

Para abrir el notebook con JupyterLab:

```powershell
.\.venv\Scripts\python.exe -m jupyterlab code/proyecto_final.ipynb
```

También puedes abrirlo en VS Code, seleccionar el intérprete de `.venv` y ejecutar las celdas en orden.

## Archivos

- `code/proyecto_mlp.py`: código fuente.
- `code/proyecto_final.ipynb`: notebook que utiliza el mismo código.
- `code/requirements.txt`: dependencias.
- `code/resultados/`: resultados del entrenamiento y evaluación.
- `code/resultados_preprocesamiento/`: revisión inicial del dataset.
- `code/docu-reporte/`: información de apoyo.
- `Informacion_para_reporte_EOG_MLP.docx`: conceptos y explicaciones en Word.
- `Portada.docx`: base para elaborar el reporte.

En la raíz también están el dataset original, el artículo de referencia, las instrucciones y la rúbrica.
