import base64
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import vertexai
from vertexai.generative_models import GenerativeModel

# 1. AUTENTICACIÓN CON GMAIL
# Define los permisos necesarios. 'gmail.readonly' es para solo lectura.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

creds = None
# El archivo token.json almacena los tokens de acceso y actualización del usuario.
# Se crea automáticamente cuando el flujo de autorización se completa por primera vez.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# Si no hay credenciales (válidas), permite que el usuario inicie sesión.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        # Carga las credenciales del cliente desde el archivo descargado de Google Cloud Console.
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Guarda las credenciales para la próxima ejecución.
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Construye el objeto de servicio para interactuar con la API de Gmail.
service = build('gmail', 'v1', credentials=creds)

# 2. EXTRAER TODOS LOS CORREOS DE UN REMITENTE ESPECÍFICO DEL ÚLTIMO MES
print("Buscando correos de serviciopse@achcolombia.com.co del último mes...")
all_messages = []
page_token = None

# Bucle para obtener todas las páginas de resultados.
while True:
    # Modifica la consulta 'q' para buscar por remitente y por fecha (últimos 30 días).
    results = service.users().messages().list(
        userId='me',
        q='from:serviciopse@achcolombia.com.co newer_than:30d',
        pageToken=page_token
    ).execute()
    
    messages = results.get('messages', [])
    all_messages.extend(messages)
    
    # Si 'nextPageToken' no está en la respuesta, significa que hemos llegado a la última página.
    page_token = results.get('nextPageToken')
    if not page_token:
        break

print(f"Se encontraron {len(all_messages)} correos.")

# 3. PROCESAR Y ENVIAR A GEMINI
# Configura la autenticación para Vertex AI (Gemini).
# Asegúrate de estar autenticado en gcloud: `gcloud auth application-default login`
# NOTA: El uso de la API de Vertex AI requiere que la facturación esté habilitada en tu proyecto de Google Cloud.
vertexai.init(project="pfm-email", location="us-central1")
model = GenerativeModel("gemini-1.5-flash-001") # O el modelo que prefieras

if not all_messages:
    print("No se encontraron correos para analizar.")
else:
    for message in all_messages:
        # Obtiene el contenido completo de cada mensaje.
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg['payload']
        
        data = ''
        # Extraer el cuerpo del correo (maneja correos multipart).
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    break # Usa la primera parte de texto plano que encuentre.
        else:
            # Si no es multipart, el cuerpo está directamente en el payload.
            if 'data' in payload['body']:
                data = payload['body']['data']

        # Si se encontró contenido, decodifícalo.
        if data:
            # Decodificar el contenido de base64 a texto.
            text = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            
            # 4. ENVIAR A GEMINI PARA ANÁLISIS
            prompt = f"""
            Analiza el siguiente correo electrónico y extrae los puntos clave en una lista.
            No incluyas saludos ni despedidas. Sé conciso.

            Correo:
            {text}
            """
            
            try:
                response = model.generate_content(prompt)
                print("--- ANÁLISIS DEL CORREO ---")
                print(response.text)
                print("--------------------------\n")
            except Exception as e:
                print(f"Error al analizar correo con Gemini: {e}")
        else:
            print(f"No se pudo extraer texto del correo con ID: {message['id']}")
