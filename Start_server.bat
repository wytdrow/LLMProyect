@echo off
REM Script de inicio automático para Flask Server (Ollama) y ngrok
REM Autor: Gemini
REM
REM PASOS ANTES DE EJECUTAR:
REM 1. Asegúrate de que Ollama esté instalado y el modelo 'llama3:8b' esté descargado.
REM 2. Asegúrate de que Flask Server (server.py) esté en esta misma carpeta.
REM 3. Asegúrate de que ngrok esté instalado y agregado a la variable PATH.
REM 4. Asegúrate de que tu entorno virtual (.venv) se llame ".venv".

echo ===================================================
echo 🚀 INICIANDO SERVIDOR Y TUNEL NGROK...
echo ===================================================

REM 1. Activa el entorno virtual
call .venv\Scripts\activate

REM 2. Inicia el servidor Flask en una nueva ventana (cmd /k mantiene la ventana abierta)
start "Flask Server (Ollama)" cmd /k "python server.py"

REM Espera 5 segundos para que Flask se inicialice antes de iniciar ngrok.
timeout /t 5 /nobreak > nul

REM 3. Inicia ngrok en una nueva ventana (cmd /k mantiene la ventana abierta)
REM **IMPORTANTE: ngrok abrirá una ventana. COPIA la URL HTTPS para usarla en client.py**
start "Ngrok Tunnel" cmd /k "ngrok http 5000"

echo.
echo ---------------------------------------------------
echo ✅ Proceso iniciado.
echo ⚠️ Vuelve a la ventana de NGROK y COPIA la URL HTTPS.
echo    Pégala en la variable SERVER_URL del archivo client.py.
echo ---------------------------------------------------
echo.

pause
exit
