import os
from main import redis
import shortuuid
import cv2
import numpy as np
from main import redis as redis_db
from main import sports, sports_name_list
from main.models.event import event

def generate_video_source(event_id, video_source_index):
    key_video_source = f'{event_id}-video_sources-{str(video_source_index)}'
    while not int(redis_db.get(f'{event_id}-stop')):
        frame_bytes = redis.get(key_video_source)
        if frame_bytes:
            # Convertir los bytes del frame a formato de imagen
            # nparr = np.frombuffer(frame_bytes, np.uint8)
            # frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # Generar el frame para la fuente de video HTTP
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')