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

## ⚙️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

* [Python 3.9](https.python.org/downloads/) o superior.
* [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (para la herramienta `gcloud`).
* Una cuenta de Google Cloud con un proyecto activo.

## 🚀 Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto:

### 1. Clona el Repositorio
```bash
git clone <URL-de-tu-repositorio>
cd pfm-gemini
