import base64
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import vertexai
from vertexai.generative_models import GenerativeModel

# 1. AUTENTICACIÓN CON GMAIL
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly'] # Solo permiso de lectura

creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        # Aquí usarás tu archivo credentials.json descargado
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Construye el servicio de la API de Gmail
service = build('gmail', 'v1', credentials=creds)

# 2. EXTRAER CORREOS
# Ejemplo: buscar los últimos 20 correos de 'un-remitente@ejemplo.com'
results = service.users().messages().list(userId='me', q='from:un-remitente@ejemplo.com', maxResults=20).execute()
messages = results.get('messages', [])

# 3. PROCESAR Y ENVIAR A GEMINI
# Configura la autenticación para Vertex AI (Gemini)
# Debes estar autenticado en gcloud: `gcloud auth application-default login`
vertexai.init(project="pfm-email", location="us-central1")
model = GenerativeModel("gemini-1.5-flash-001") # O el modelo que prefieras

if not messages:
    print("No se encontraron correos.")
else:
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg['payload']
        
        # Extraer el cuerpo del correo (simplificado)
        if 'parts' in payload:
            part = payload['parts'][0]
            data = part['body']['data']
        else:
            data = payload['body']['data']

        # Decodificar el contenido
        text = base64.urlsafe_b64decode(data).decode('utf-8')
        
        # 4. ENVIAR A GEMINI PARA ANÁLISIS
        prompt = f"""
        Analiza el siguiente correo electrónico y extrae los puntos clave en una lista.
        No incluyas saludos ni despedidas. Sé conciso.

        Correo:
        {text}
        """
        
        response = model.generate_content(prompt)
        print("--- ANÁLISIS DEL CORREO ---")
        print(response.text)
        print("--------------------------\n")