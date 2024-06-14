import redis
import cv2
import numpy as np
import subprocess
import time

# Configuración de Redis
redis_host = 'localhost'
redis_port = 6379
redis_password = ''
redis_key = 'aG49BTMTqPHeAB3wXdmFho-video_frame'

# Configuración del servidor RTMP
rtmp_url = 'rtmp://localhost/live/stream'

def get_frame_from_redis():
    try:
        frame_data = r.get(redis_key)
        if frame_data:
            np_arr = np.frombuffer(frame_data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            return frame
        else:
            return None
    except Exception as e:
        print(f"Error al obtener el frame de Redis: {e}")
        return None

# Conectar a Redis
r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

# Crear el proceso de ffmpeg
ffmpeg_command = [
    'ffmpeg',
    '-y',
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', '1920x1080',
    '-r', '30',
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-f', 'flv',
    rtmp_url
]

process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

try:
    while True:
        start_time = time.time()
        frame = get_frame_from_redis()
        if frame is not None:
            if frame.shape[1] != 1920 or frame.shape[0] != 1080:
                frame = cv2.resize(frame, (1920, 1080))
            process.stdin.write(frame.tobytes())
        else:
            print("No se obtuvo frame de Redis.")
        
        time.sleep(1/35)
except KeyboardInterrupt:
    print("Transmisión interrumpida por el usuario.")
finally:
    process.stdin.close()
    process.wait()
