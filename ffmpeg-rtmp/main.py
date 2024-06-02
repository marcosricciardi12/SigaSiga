import requests
import subprocess
import re

# URL de la fuente de video HTTP
video_url = "https://localhost:5000/streaming/video_feed/?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNzMyMTkyMSwianRpIjoiMDM4ZTViOGYtNTQyMS00OWU0LWEzZDctYjBmNTViMDFiMDc5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VyX2lkIjoiZDVjMDE3OGEtNjc2OS00MTg5LWFjNzktNDc3ZTUzODJjNTZlIn0sIm5iZiI6MTcxNzMyMTkyMSwiY3NyZiI6IjhiNWU5ZTQzLWIxNTYtNDc4YS1hOTA5LTQ5ZmEwNzk3Y2FmMyIsImV4cCI6MTcxNzMzNjMyMX0.ZtLZwD7KeI5BUzdQoS_-2QcwwMsxbns0YxufuIAG5as"


# Comando de ffmpeg para transmitir al servidor RTMP
ffmpeg_command = [
    'ffmpeg',
    '-re',  # Modo de entrada en tiempo real
    '-i', '-',  # Entrada desde la tubería estándar
    '-c:v', 'copy',  # No se realiza ninguna conversión de video
    '-f', 'flv',  # Formato de salida FLV
    'rtmp://a.rtmp.youtube.com/live2/9kvw-ujak-cp6w-4qwg-cx62'  # URL del servidor RTMP
]

# Ejecutar ffmpeg como un proceso
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

# Realizar la solicitud HTTP a la fuente de video con stream=True
response = requests.get(video_url, stream=True, verify=False)
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