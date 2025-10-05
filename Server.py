# Archivo: server.py
# Este script levanta un servidor Flask que expone el modelo Llama 3 (a través de Ollama)
# Permite el acceso remoto y mantiene el historial de chat para cada usuario.

import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from ollama import Client # ⬅️ CORRECCIÓN: Quitamos OllamaBaseException para evitar el ImportError.

# --- CONFIGURACIÓN DE SEGURIDAD Y MODELO ---
MODELO_LLM = "llama3:8b" 
API_KEY_SECRETA = "MiClaveSuperSegura123" # ⬅️ IMPORTANTE: ¡Cambia esto por una clave más fuerte!
# ------------------------------------------

# --- Inicialización del Cliente Ollama ---
try:
    # Se conecta al servicio Ollama que debe estar corriendo localmente en el puerto 11434
    ollama_client = Client()
    ollama_client.list() 
    print("✅ Conexión con Ollama establecida correctamente.")
except Exception as e: # ⬅️ Usamos Exception genérico para mayor compatibilidad.
    # Si la lista falla, asumimos que el servicio Ollama no está activo.
    print(f"❌ ERROR CRÍTICO: No se pudo conectar al servicio de Ollama en localhost:11434.")
    print(f"Detalles del error: {e}")
    print("Asegúrate de que el servidor 'ollama run llama3:8b' esté activo ANTES de iniciar Flask.")
    exit(1)


# --- Configuración de Flask y Almacenamiento de Historial ---
app = Flask(__name__)
CORS(app) # Habilita CORS para permitir acceso desde otros dominios (navegadores)

# Diccionario para almacenar el historial de chat de cada sesión.
# La clave es el 'session_id' enviado por el cliente.
chat_history = {}


# --- Ruta de Chat Principal ---

@app.route("/chat", methods=["POST"])
def chat():
    # 1. Verificación de la Clave API (Seguridad)
    cliente_api_key = request.headers.get("X-API-Key")
    if cliente_api_key != API_KEY_SECRETA:
        return jsonify({"response": "Acceso denegado. Clave API incorrecta."}), 401

    # 2. Extracción y validación de datos
    data = request.get_json()
    mensaje = data.get("mensaje", "")
    session_id = data.get("session_id", "default_session")

    if not mensaje or not mensaje.strip():
        return jsonify({"response": "No enviaste ningún mensaje."}), 400

    print(f"[{time.strftime('%H:%M:%S')}] Recibido (Session {session_id}): '{mensaje[:50]}...'")

    # 3. Gestión del historial
    if session_id not in chat_history:
        # Inicializa el historial para la nueva sesión
        chat_history[session_id] = []

    # Agrega el mensaje actual del usuario al historial
    chat_history[session_id].append({"role": "user", "content": mensaje})

    # 4. Llamada al modelo Ollama con el historial completo
    try:
        response = ollama_client.chat(
            model=MODELO_LLM,
            messages=chat_history[session_id], # Pasa toda la conversación para contexto
            options={
                "temperature": 0.8
            }
        )
        
        salida = response['message']['content']

        # 5. Agrega la respuesta del asistente al historial
        chat_history[session_id].append({"role": "assistant", "content": salida})


    except Exception as e: # ⬅️ Usamos Exception genérico para manejar cualquier fallo del LLM
        print(f"Error al ejecutar el modelo Ollama: {e}")
        # Retira el último mensaje de usuario si la llamada falla
        chat_history[session_id].pop() 
        return jsonify({"response": f"Error del modelo Ollama: {e}"}), 500

    return jsonify({"response": salida})

if __name__ == "__main__":
    print("-" * 50)
    print(f"🔥 Servidor de Ollama (Modelo: {MODELO_LLM})")
    print(f"🔑 API Key: {API_KEY_SECRETA}")
    print("🌐 Dirección local: http://0.0.0.0:5000")
    print("-" * 50)
    
    # Escucha en 0.0.0.0 (todas las interfaces) para que ngrok lo pueda alcanzar
    app.run(host="0.0.0.0", port=5000)
