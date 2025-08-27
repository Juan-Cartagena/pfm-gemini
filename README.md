# Analizador de Finanzas Personales con Gemini (PFM-Gemini)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-Enabled-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Este proyecto utiliza el poder de los modelos generativos de Google (Gemini) para analizar correos electrónicos de una cuenta de Gmail, con el objetivo de extraer y procesar información financiera de manera automatizada. Es una herramienta de "Personal Finance Management" (PFM) que te permite obtener insights de tus gastos, facturas y transacciones directamente desde tu bandeja de entrada.

---

## ▶️ Características

* **Conexión Segura a Gmail**: Utiliza OAuth 2.0 para acceder a los correos de forma segura, respetando la privacidad y los permisos del usuario.
* **Filtrado Avanzado de Correos**: Permite definir criterios de búsqueda específicos (remitente, asunto, etiquetas, etc.) para procesar únicamente los correos relevantes.
* **Análisis con IA Generativa**: Envía el contenido de los correos a la API de Gemini para realizar tareas complejas como:
    * Resumir gastos.
    * Extraer montos, fechas de vencimiento y conceptos de facturas.
    * Clasificar transacciones por categoría.
* **Modular y Personalizable**: El script de Python está diseñado para ser fácilmente adaptable a diferentes necesidades de análisis.

---

## ⚙️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

* [Python 3.9](https://www.python.org/downloads/) o superior.
* [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (para la herramienta `gcloud`).
* Una cuenta de Google Cloud con un proyecto activo.

---

## 🚀 Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto:

### 1. Clona el Repositorio

```bash
git clone <URL-de-tu-repositorio>
cd pfm-gemini
```

### 2. Configura el Entorno Virtual

Es una buena práctica trabajar dentro de un entorno virtual.

```bash
# Crear el entorno
python -m venv .venv

# Activar el entorno
# En Windows (Git Bash):
source .venv/Scripts/activate
# En macOS/Linux:
# source .venv/bin/activate
```

### 3. Instala las Dependencias

Crea un archivo `requirements.txt` con el siguiente contenido:

```txt
--upgrade
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
google-cloud-aiplatform
```

Luego, instálalo usando pip:

```bash
pip install -r requirements.txt
```

### 4. Configura tu Proyecto de Google Cloud

1.  **Habilita las APIs**: En tu proyecto de Google Cloud, asegúrate de tener habilitadas la **Gmail API** y la **Vertex AI API**.
2.  **Configura la Pantalla de Consentimiento OAuth**:
    * Ve a `APIs y servicios > Pantalla de consentimiento de OAuth`.
    * Configúrala como **Externa** y agrega tu propia cuenta de correo como **usuario de prueba**.
3.  **Obtén las Credenciales**:
    * Ve a `APIs y servicios > Credenciales`.
    * Crea un **ID de cliente de OAuth** de tipo **"Aplicación de escritorio"**.
    * Descarga el archivo JSON y **renómbralo a `credentials.json`**.
    * **¡IMPORTANTE!** Coloca este archivo en la raíz de tu proyecto. No lo subas a Git.

### 5. Autenticación Local

1.  **Autentica la gcloud CLI**: Este paso le da permiso a tu script para usar la API de Gemini (Vertex AI).

    ```bash
    gcloud auth application-default login
    ```

2.  **Autoriza el Acceso a Gmail**: La primera vez que ejecutes el script `analizador_correos.py`, se abrirá una ventana en tu navegador pidiéndote que autorices el acceso a tu cuenta de Gmail. Al completarlo, se creará un archivo `token.json` en tu proyecto.

---

## 💻 Uso

Una vez completada la configuración, puedes ejecutar el script de análisis:

```bash
python analizador_correos.py
```

El script se conectará a tu cuenta de Gmail, buscará los correos que coincidan con la consulta definida en el código y enviará cada uno a Gemini para su análisis. Los resultados se imprimirán en la consola.

Puedes modificar la consulta de búsqueda dentro del archivo `.py` para adaptarla a tus necesidades:

```python
# Ejemplo dentro de analizador_correos.py
results = service.users().messages().list(
    userId='me', 
    q='from:facturacion@tienda.com is:unread', # Modifica esta consulta
    maxResults=10
).execute()
```

---

## 🔒 Seguridad

La seguridad de tus credenciales y tokens es fundamental.

* El archivo `.gitignore` está configurado para **ignorar `credentials.json` y `token.json`**.
* **Nunca** compartas estos archivos ni los subas a repositorios públicos. Contienen información sensible que da acceso a tus servicios de Google.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
