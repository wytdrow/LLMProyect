# Archivo: client.py
# Este script se ejecuta en la máquina remota.

import requests
import uuid

# --- CONFIGURACIÓN ---
# ⚠️ REEMPLAZA esta URL con la que te da ngrok (¡debe terminar en /chat!)
SERVER_URL = "https://eusebia-concerted-erectly.ngrok-free.dev/chat" 

# Debe coincidir exactamente con la API_KEY_SECRETA en server.py
API_KEY = "MiClaveSuperSegura123" 
# ---------------------

# Generamos un ID de sesión único al inicio del cliente
# Este ID asegura que el servidor guarde nuestro historial de chat.
SESSION_ID = str(uuid.uuid4())

def enviar_mensaje(mensaje):
    """Envía el mensaje al servidor Flask a través de ngrok."""
    
    # Preparamos los datos a enviar
    payload = {
        "mensaje": mensaje,
        "session_id": SESSION_ID
    }
    
    # Preparamos los encabezados con la clave API
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    try:
        # Hacemos la solicitud POST al servidor
        response = requests.post(SERVER_URL, json=payload, headers=headers)
        
        # Si la respuesta no fue exitosa (código 4xx o 5xx)
        response.raise_for_status() 
        
        # Devolvemos la respuesta del modelo
        return response.json().get("response", "No hay respuesta del modelo.")
        
    except requests.exceptions.HTTPError as errh:
        # Maneja errores HTTP (401, 404, 500, etc.)
        return f"Error HTTP (clave incorrecta o servidor falló): {errh}"
    except requests.exceptions.ConnectionError as errc:
        # Maneja fallos de conexión (ngrok caído, URL mal escrita, etc.)
        return f"Error de Conexión: No se pudo alcanzar el servidor. Asegúrate de que ngrok esté activo y la URL sea correcta. Detalle: {errc}"
    except requests.exceptions.RequestException as e:
        # Maneja otros errores de la solicitud
        return f"Error desconocido en la solicitud: {e}"

print("--- Cliente Cerebro ---")
print(f"Sesión ID: {SESSION_ID}")
print(f"Conectando a: {SERVER_URL}")
print("Escribe 'salir' para terminar")

while True:
    usuario = input("\nTú: ")
    if usuario.lower() == "salir":
        break
    
    respuesta = enviar_mensaje(usuario)
    print("Cerebro:", respuesta)
