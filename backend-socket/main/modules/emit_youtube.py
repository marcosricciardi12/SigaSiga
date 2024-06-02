import os
import subprocess
import time


def capture_frame(redis_client, event_id):
    # Capturar el frame desde Redis
    frame_bytes = redis_client.get(f'{event_id}-video_frame')  # Ajusta 'frame_key' a la clave donde se guarda el frame en Redis
    
    # Verificar si se recibió un frame válido
    if frame_bytes:
        return frame_bytes
    else:
        return None

# Función para generar y transmitir el video a través de ffmpeg
def generate_and_stream_video(redis_client, event_id):
    # Comando de ffmpeg para generar el video y transmitirlo a través de RTMP
    youtube_rtmp_key = redis_client.get(f'{event_id}-youtube_rtmp_key').decode('utf-8')

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
        f'rtmp://a.rtmp.youtube.com/live2/{youtube_rtmp_key}'  # URL del servidor RTMP de YouTube
    ]

    # Iniciar ffmpeg como proceso
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

    # Bucle para capturar y transmitir frames continuamente
    
    try:
        print("Start youtube streaming")
        while int(redis_client.get(f'{event_id}-youtube_streaming_status')) and not int(redis_client.get(f'{event_id}-stop')):
            time.sleep(1/30)
            # Capturar el frame desde Redis
            frame_bytes = capture_frame(redis_client, event_id)

            # Verificar si se recibió un frame válido
            if frame_bytes:
                # Escribir el frame en el proceso de ffmpeg
                ffmpeg_process.stdin.write(frame_bytes)
                ffmpeg_process.stdin.flush()  # Limpiar el buffer de entrada
        print("Stop youtube streaming")
        ffmpeg_process.kill()
        os._exit(0)
    except:
        print("Stop youtube streaming")
        ffmpeg_process.kill()
        os._exit(0)

def emit_to_youtube(redis_client, event_id):
    generate_and_stream_video(redis_client, event_id)