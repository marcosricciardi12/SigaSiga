import base64
import time

import cv2
import numpy as np
from main import redis as redis_db

def generate_video_source(event_id, socket_client_id):
    key_video_source = f'{event_id}-socket_video_sources-{str(socket_client_id)}'
    while not int(redis_db.get(f'{event_id}-stop')):
        time.sleep(1/30)
        frame_bytes = get_frame_from_redis(key_video_source)
        if frame_bytes:
            yield (b'--frame\r\n'
                b'Content-Type: image/webp\r\n\r\n' + frame_bytes + b'\r\n')
            
def get_frame_from_redis(key):
    # Obtener el frame almacenado en Redis
    encoded_frame = redis_db.get(key)
    if encoded_frame is None:
        print("No frame found in Redis for the given key.")
        return None

    # Decodificar el frame de base64
    webp_frame = base64.b64decode(encoded_frame)

    # Convertir los bytes del frame WebP a una matriz de imagen que OpenCV pueda usar

    return webp_frame