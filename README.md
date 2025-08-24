# Proyecto de Análisis de Inversiones

Este proyecto es una aplicación web diseñada para ayudar a los usuarios a tomar decisiones de inversión informadas mediante el seguimiento y análisis de datos del mercado de acciones. La solución extrae datos de acciones mediante web scraping, los almacena y los presenta en un dashboard interactivo con visualizaciones y gráficos.

## Características

- **Web Scraping de Datos de Acciones:** Extrae información financiera actualizada de acciones de Yahoo Finance.
- **Almacenamiento de Datos:** Guarda los datos extraídos en archivos CSV para su posterior análisis.
- **API de Backend:** Una API RESTful construida con Flask que proporciona los datos de las acciones al frontend.
- **Dashboard Interactivo:** Una interfaz de usuario web para visualizar los datos de las acciones y los gráficos de precios.
- **Visualización de Datos:** Genera gráficos de precios para acciones individuales.

## Estructura del Proyecto

El proyecto está organizado en los siguientes directorios:

- `backend/`: Contiene la lógica del servidor y el web scraper.
  - `scraper.py`: Script para extraer datos de acciones.
  - `app.py`: Aplicación Flask que sirve la API y el frontend.
  - `requirements.txt`: Dependencias de Python para el backend.
- `frontend/`: Contiene los archivos de la interfaz de usuario.
  - `index.html`: Archivo HTML principal.
  - `styles.css`: Hoja de estilos CSS.
  - `scripts.js`: Lógica de JavaScript para el frontend.
- `data/`: Directorio donde se almacenan los datos de las acciones en formato CSV (se crea automáticamente).
- `.venv/`: Directorio para el entorno virtual de Python.

## Instalación y Ejecución

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

### Prerrequisitos

- Python 3.x
- pip (generalmente viene con Python)

### 1. Clonar el Repositorio

```bash
git clone https://github.com/hermesvillarreal/AnalisisInversiones.git
cd AnalisisInversiones
```

### 2. Configurar el Entorno Virtual y las Dependencias

Para mantener las dependencias del proyecto aisladas, se recomienda utilizar un entorno virtual.

```bash
# Crear un entorno virtual
python -m venv .venv

# Activar el entorno virtual
# En Windows:
.venv\Scripts\activate
# En macOS/Linux:
# source .venv/bin/activate

# Instalar las dependencias de Python
pip install -r backend/requirements.txt
```

### 3. Ejecutar el Web Scraper

Para obtener los datos más recientes de las acciones, ejecuta el script de scraping. Este paso es necesario antes de iniciar el servidor por primera vez.

```bash
python backend/scraper.py
```

Este comando extraerá los datos de los tickers predefinidos en `scraper.py` y los guardará en la base de datos SQLite `stocks.db` dentro del directorio `data/`.


### 4. Iniciar el Servidor Web

Una vez que tengas los datos, puedes iniciar el servidor Flask para visualizar el dashboard.

```bash
python backend/app.py
```

El servidor se iniciará en modo de depuración y estará disponible en `http://127.0.0.1:5000`.

## Cómo Usar la Aplicación

### Visualización de Datos

1.  Abre tu navegador web y navega a `http://127.0.0.1:5000`.
2.  Verás el **Dashboard de Acciones**, que muestra una cuadrícula con las tarjetas de información para cada acción que ha sido registrada. Cada tarjeta incluye:
    - **Ticker:** El símbolo de la acción (ej. AAPL).
    - **Price:** El precio de mercado actual.
    - **Previous Close:** El precio de cierre del día anterior.
    - **Open:** El precio de apertura del día.
    - **Volume:** El volumen de acciones negociadas.
    - **Market Cap:** La capitalización de mercado de la empresa.
    - **Timestamp:** Fecha y hora en que se registró el dato.

### Interpretación de los Gráficos

1.  Debajo de la cuadrícula de datos, encontrarás una sección para **visualizar el gráfico de precios** de una acción específica.
2.  Usa el **menú desplegable** para seleccionar el ticker de la acción que deseas analizar.
3.  El gráfico se cargará automáticamente, mostrando la evolución histórica del precio de la acción según los datos almacenados en la base de datos SQLite.

## Futuras Mejoras

- **Gráficos Avanzados:** Implementar librerías como Chart.js o D3.js para crear gráficos más interactivos (gráficos de velas, medias móviles, etc.).
- **Automatización de Tareas:** Configurar una tarea programada (cron job) para ejecutar el scraper automáticamente a intervalos regulares.
- **Personalización de Tickers:** Permitir a los usuarios añadir y eliminar los tickers que desean seguir a través de la interfaz de usuario.
- **Análisis Técnico:** Añadir indicadores de análisis técnico comunes (RSI, MACD) a los gráficos.
