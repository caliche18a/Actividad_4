# Analisis interactivo de mortalidad en Colombia 2019

## Estudiantes de la maestría en Inteligencia Articial
- Carlos Enrique Jiménez Avendaño
- Gustavo Alberto Guerrero Polanco
- Osman Angulo

## Sobre la aplicación web

Aplicacion web desarrollada con Python, Dash y Plotly para explorar los registros de mortalidad no fetal en Colombia durante 2019. El proyecto usa los anexos del DANE, la codificacion CIE-10 de causas de muerte, la division politico-administrativa DIVIPOLA y un archivo GeoJSON de departamentos.

![Captura del dashboard](docs/screenshots/dashboard.png)

## Objetivo

Analizar patrones regionales, temporales, demograficos y causales de mortalidad en Colombia para 2019 mediante un dashboard interactivo. La aplicacion permite filtrar por departamento, sexo y rango de meses, actualizando dinamicamente los indicadores, graficos y tabla.

## Estructura del proyecto

```text
.
|-- app.py
|-- config.py
|-- requirements.txt
|-- Procfile
|-- render.yaml
|-- runtime.txt
|-- data/
|   |-- Anexo1.NoFetal2019_CE_15-03-23.xlsx
|   |-- Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx
|   |-- Divipola_CE_.xlsx
|   |-- Colombia.geo.json
|-- models/
|   |-- age_groups.py
|   |-- analytics.py
|   |-- data_loader.py
|-- controllers/
|   |-- callbacks.py
|   |-- dashboard_state.py
|-- views/
|   |-- figures.py
|   |-- layout.py
|-- assets/
|   |-- styles.css
|-- docs/
|   |-- screenshots/
|       |-- dashboard.png
|-- scripts/
    |-- run_local.py
```

## Requisitos

- Python 3.12
- Dash
- Plotly
- Pandas
- OpenPyXL
- Gunicorn, para despliegue en Linux/Render

Las versiones compatibles estan definidas en `requirements.txt`.

## Instalacion local

```bash
git clone https://github.com/caliche18a/Actividad_4
cd Actividad_4
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

En Windows, si el puerto 8050 esta ocupado, puede ejecutarse:

```bash
set PORT=3000
python scripts/run_local.py
```

## Despliegue en Render

1. Subir el proyecto a GitHub, incluyendo `app.py`, `requirements.txt`, `Procfile`, `render.yaml`, carpetas `models/`, `controllers/`, `views/`, `assets/` y `data/`.
2. Crear un nuevo servicio Web en Render y conectar el repositorio.
3. Usar ambiente Python.
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:server`
6. Esperar el despliegue y copiar la URL publica para la entrega.

El archivo `render.yaml` deja estos valores listos para despliegue tipo blueprint.

## Software utilizado

- Python para procesamiento de datos.
- Pandas y OpenPyXL para lectura y transformacion de archivos Excel.
- Plotly Graph Objects para las visualizaciones interactivas.
- Dash para la aplicacion web.
- HTML/CSS en `assets/styles.css` para presentacion visual.
- Gunicorn para servir la app en PaaS.

## Visualizaciones y resultados

- Mapa por departamento: Bogota D.C., Antioquia y Valle del Cauca concentran los mayores totales de muertes registradas en 2019.
- Linea mensual: diciembre registra el mayor total mensual, con 21.678 muertes; febrero es el mes mas bajo, con 17.974.
- Barras de homicidios X95: Santiago de Cali lidera los homicidios por agresion con disparo de otras armas de fuego y no especificadas, con 971 casos; le siguen Bogota D.C. y Medellin.
- Grafico circular: muestra los municipios con menor mortalidad registrada en el archivo, todos con 1 caso dentro del periodo analizado.
- Tabla de causas: la primera causa es `I219`, infarto agudo del miocardio sin otra especificacion, con 35.088 casos.
- Barras apiladas por sexo: en la mayoria de departamentos el total masculino supera al femenino, con los mayores volumenes en Bogota D.C., Antioquia y Valle del Cauca.
- Histograma por edad: la vejez concentra el mayor volumen de defunciones, seguida por longevidad/centenarios.

## Datos de entrega

- Integrantes: completar con nombres completos.
- URL de la aplicacion desplegada: completar despues del despliegue.
- URL del repositorio en GitHub: completar despues de subir el proyecto.
