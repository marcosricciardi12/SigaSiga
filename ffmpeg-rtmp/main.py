import requests
import subprocess
import re

# URL de la fuente de video HTTP
video_url = "http://localhost:5000/streaming/video_feed/cBpLJnNv2mX9QzuX3whqg7"

# Comando de ffmpeg para transmitir al servidor RTMP
ffmpeg_command = [
    'ffmpeg',
    '-re',  # Modo de entrada en tiempo real
    '-i', '-',  # Entrada desde la tubería estándar
    '-c:v', 'copy',  # No se realiza ninguna conversión de video
    '-f', 'flv',  # Formato de salida FLV
    'rtmp://localhost/live/stream'  # URL del servidor RTMP
]

# Ejecutar ffmpeg como un proceso
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

# Realizar la solicitud HTTP a la fuente de video con stream=True
response = requests.get(video_url, stream=True)
print(response)
# Iterar indefinidamente para capturar y transmitir los frames en tiempo real
while True:
    # Leer el próximo chunk de datos de la respuesta HTTP
    
    chunk = response.raw.read(1024)
    if not chunk:
        # Finalizar el bucle si no hay más datos disponibles
        break
    
    # Buscar el patrón de delimitador de frames
    boundary_pattern = re.compile(b'\r\n--frame\r\n')
    frame_start_indices = [match.start() for match in boundary_pattern.finditer(chunk)]
    
    # Procesar cada frame encontrado
    for i, start_index in enumerate(frame_start_indices):
        # Encontrar el inicio de un nuevo frame
        frame_data = chunk[start_index + len(b'\r\n--frame\r\n'):]
        # Escribir el frame en el proceso de ffmpeg
        ffmpeg_process.stdin.write(frame_data)

# Finalizar el proceso de ffmpeg
ffmpeg_process.stdin.close()
ffmpeg_process.wait()