import redis
import subprocess
import time
# Conexión a Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Función para capturar el frame desde Redis
def capture_frame():
    # Capturar el frame desde Redis
    frame_bytes = redis_client.get('ABDkAAoYx8w4bfXjxHDjT9-video_frame')  # Ajusta 'frame_key' a la clave donde se guarda el frame en Redis
    
    # Verificar si se recibió un frame válido
    if frame_bytes:
        return frame_bytes
    else:
        return None

# Función para generar y transmitir el video a través de ffmpeg
def generate_and_stream_video():
    # Comando de ffmpeg para generar el video y transmitirlo a través de RTMP
    ffmpeg_command = [
        'ffmpeg', 
        '-f', 'image2pipe',  # Formato de entrada como pipe
        '-i', 'pipe:0',  # Usar la entrada estándar para leer los datos de imagen
        '-f', 'pulse', 
        '-i', 'alsa_output.usb-Kingston_HyperX_Cloud_Stinger_Core___7.1_0000000000000000-00.analog-stereo.monitor',  # URL de la fuente de audio
        '-c:v', 'libx264',  # Códec de video
        '-preset', 'ultrafast',  # Preset de codificación de video
        '-tune', 'zerolatency',  # Configuración de latencia cero
        '-pix_fmt', 'yuv420p',  # Formato de píxeles de salida
        '-r', '30',  # Frecuencia de fotogramas de salida
        '-c:a', 'aac',  # Códec de audio
        '-f', 'flv',  # Formato de salida como FLV
        'rtmp://a.rtmp.youtube.com/live2/9kvw-ujak-cp6w-4qwg-cx62'  # URL del servidor RTMP de YouTube
    ]

    # Iniciar ffmpeg como proceso
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

    # Bucle para capturar y transmitir frames continuamente
    while True:
        time.sleep(1/30)
        # Capturar el frame desde Redis
        frame_bytes = capture_frame()

        # Verificar si se recibió un frame válido
        if frame_bytes:
            # Escribir el frame en el proceso de ffmpeg
            ffmpeg_process.stdin.write(frame_bytes)
            ffmpeg_process.stdin.flush()  # Limpiar el buffer de entrada

# Llamar a la función para generar y transmitir el video
generate_and_stream_video()