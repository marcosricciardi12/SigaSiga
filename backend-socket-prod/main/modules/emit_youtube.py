import os
import subprocess
import time
import requests
import re

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

    # ffmpeg_command = [
    #     'ffmpeg', 
    #     '-f', 'image2pipe',  # Formato de entrada como pipe
    #     '-i', 'pipe:0',  # Usar la entrada estándar para leer los datos de imagen
    #     '-f', 'pulse', 
    #     '-i', 'alsa_output.usb-Kingston_HyperX_Cloud_Stinger_Core___7.1_0000000000000000-00.analog-stereo.monitor',  # URL de la fuente de audio
    #     '-c:v', 'libx264',  # Códec de video
    #     '-preset', 'ultrafast',  # Preset de codificación de video
    #     '-tune', 'zerolatency',  # Configuración de latencia cero
    #     '-pix_fmt', 'yuv420p',  # Formato de píxeles de salida
    #     '-r', '30',  # Frecuencia de fotogramas de salida
    #     '-c:a', 'aac',  # Códec de audio
    #     '-f', 'flv',  # Formato de salida como FLV
    #     f'rtmp://a.rtmp.youtube.com/live2/{youtube_rtmp_key}'  # URL del servidor RTMP de YouTube
    # ]

    ffmpeg_command = [
        'ffmpeg',
        '-thread_queue_size', '2048',  # Aumentar el tamaño de la cola de mensajes del hilo para video
        '-f', 'image2pipe',  # Formato de entrada como pipe
        '-i', 'pipe:0',  # Usar la entrada estándar para leer los datos de imagen
        '-thread_queue_size', '2048',  # Aumentar el tamaño de la cola de mensajes del hilo para audio
        '-f', 'pulse',
        '-i', 'alsa_output.usb-Kingston_HyperX_Cloud_Stinger_Core___7.1_0000000000000000-00.analog-stereo.monitor',  # URL de la fuente de audio
        '-c:v', 'libx264',  # Códec de video
        '-preset', 'ultrafast',  # Preset de codificación de video
        '-tune', 'zerolatency',  # Configuración de latencia cero
        '-pix_fmt', 'yuv420p',  # Formato de píxeles de salida
        '-r', '30',  # Frecuencia de fotogramas de salida
        '-g', '120',  # Frecuencia de fotogramas clave (keyframe interval) (aumentado para reducir duplicados)
        '-b:v', '2500k',  # Tasa de bits de video
        '-c:a', 'aac',  # Códec de audio
        '-b:a', '128k',  # Tasa de bits de audio
        '-bufsize', '5000k',  # Tamaño del buffer
        '-maxrate', '2500k',  # Tasa de bits máxima
        '-fps_mode', 'cfr',  # Modo de sincronización de fotogramas (Constant Frame Rate)
        '-use_wallclock_as_timestamps', '1',  # Usar timestamps del reloj de pared
        '-f', 'flv',  # Formato de salida como FLV
        f'rtmp://a.rtmp.youtube.com/live2/{youtube_rtmp_key}'  # URL del servidor RTMP de YouTube
    ]

    # Iniciar ffmpeg como proceso
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

    # Bucle para capturar y transmitir frames continuamente
    
    try:
        print("Start youtube streaming")
        while int(redis_client.get(f'{event_id}-youtube_streaming_status')) and not int(redis_client.get(f'{event_id}-stop')):
            time.sleep(1/45)
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




def capture_and_stream_fromhttp(token, redis_client, event_id):
    # URL de la fuente de video HTTP
    youtube_rtmp_key = redis_client.get(f'{event_id}-youtube_rtmp_key').decode('utf-8')
    video_url = "https://localhost:5000/streaming/video_feed/" + '?token=' + token
    youtube_url = "rtmp://a.rtmp.youtube.com/live2"
    rtmp_url = youtube_url + '/' + youtube_rtmp_key
    ffmpeg_command = [
        "ffmpeg",
        "-f", "mjpeg",
        "-re",
        "-r", "30",  # Limita los fps a 30
        "-i", f"{video_url}",
        "-f", "pulse",
        "-i", "alsa_output.usb-Kingston_HyperX_Cloud_Stinger_Core___7.1_0000000000000000-00.analog-stereo.monitor",
        "-c:v", "libx264",
        # "-preset", "ultrafast",
        # "-tune", "zerolatency",
        # "-b:v", "2M",
        # "-bufsize", "2M",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-ac", "2",
        "-f", "flv",
        f"{rtmp_url}"
    ]

    # Ejecutar el comando ffmpeg
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Leer la salida y los errores del proceso
    
    print("Start youtube streaming")
    while int(redis_client.get(f'{event_id}-youtube_streaming_status')) and not int(redis_client.get(f'{event_id}-stop')):
        pass

    process.kill()
    os._exit(0)
        
def emit_to_youtube_from_http(token, redis_client, event_id):
    print("emit to yt from http : ", token)
    capture_and_stream_fromhttp(token, redis_client, event_id)
    os._exit(0)