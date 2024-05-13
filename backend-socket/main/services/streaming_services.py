import os
import time
from main import redis
import shortuuid
import cv2
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np
from main import sports, sports_name_list
from main.models.event import event
from main.services.scoreboard_services import get_scoreboard
import main.modules.remove_redis_data as remove_redis_data


def new_event_service(sport_id):
    sport_id = int(sport_id)
    selected_sport = sports_name_list[sport_id]
    event_id = str(shortuuid.uuid())

    sport = sports[sport_id]
    print(sport)
    for key in event:
        redis.set(f'{event_id}-{key}', event[key])
    redis.set(f'{event_id}-event_id', event_id)
    redis.set(f'{event_id}-sport', selected_sport)
    redis.set(f'{event_id}-sport_id', sport_id)

    for name_sport in sport:
        # print(name_sport)
        for type_info in sport[name_sport]:
            # print(type_info)
            # print(sport[name_sport][type_info])
            for attribute in sport[name_sport][type_info]:
                # print(attribute)
                redis.set(f'{event_id}-{type_info}-{attribute}', sport[name_sport][type_info][attribute])
    return read_data_event(event_id)

def read_data_event(event_id):
    for key in event:
        event[key] = redis.get(f'{event_id}-{key}')
        event[key] = event[key].decode('utf-8')
    return event

def play_event(event_id):
    value = int(True)
    redis.set(f'{event_id}-play', value)
    return "done"

def pause_event(event_id):
    value = int(False)
    redis.set(f'{event_id}-play', value)
    return "done"

#cambio stop a True, matara al streaming
def stop_event(event_id):
    value = int(True)
    redis.set(f'{event_id}-stop', value)
    remove_redis_data.delete_event(event_id)
    return {f'{event_id} Status': "Stopped and removed"}

#Implementar logica para comenzar stream
def start_event():
    event_id = str(shortuuid.uuid())
    for key in event:
        redis.set(f'{event_id}-{key}', event[key])
    return "done"

def get_sports_list():
    return {int(i): valor for i, valor in enumerate(sports_name_list)}

def generate_frames(event_id):
    video_source_index = int(redis.get(f'{event_id}-selected_video_source'))
    key_video_source = f'{event_id}-video_sources-{str(video_source_index)}'
    transparent_image = Image.open('sb.png').convert('RGBA')
    alfa = 0
    scoreboard = get_scoreboard(event_id)
    # capture = capture_list[0]
    print(os.getpid(), event_id, scoreboard)
    while not int(redis.get(f'{event_id}-stop')):
        # start_time = time.time()
        if int(redis.get(f'{event_id}-interrupt_flag')):
            redis.set(f'{event_id}-interrupt_flag', int(False))
            video_source_index = int(redis.get(f'{event_id}-selected_video_source'))
            key_video_source = f'{event_id}-video_sources-{str(video_source_index)}'
            print(video_source_index)

        frame_bytes = redis.get(key_video_source)

        # if frame_bytes:
        #     # Convertir los bytes del frame a formato de imagen
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        scoreboard = get_scoreboard(event_id)
        # transparent_image.putalpha(int(alfa))
        # if alfa >=255:
        #     alfa = 0
        # alfa += 1
        
        # Convertir el frame de OpenCV a Pillow
        pillow_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pillow_frame = Image.fromarray(pillow_frame)
        pillow_frame = pillow_frame.resize((1440, 1080))
        pillow_frame = pillow_frame.convert("RGBA")
        # Crear un lienzo de 1920x1080 y agregar el frame en el centro
        canvas = Image.new('RGBA', (1920, 1080), color='black')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(pillow_frame, ((1920 - pillow_frame.width) // 2, (1080 - pillow_frame.height) // 2))
        
        # Agregar la imagen con transparencia en el centro inferior cercano al borde
        canvas.paste(transparent_image, ((1920 - transparent_image.width) // 2, 1080 - transparent_image.height), mask=transparent_image)
        hora = str(datetime.now().strftime("%H:%M:%S"))
        draw.text((0,0), hora , fill="white", font=ImageFont.truetype("arial.ttf", 64))
        draw.text((600,930), scoreboard["local_team_short"] , fill="white", font=ImageFont.truetype("arial.ttf", 64))
        draw.text((785,930), scoreboard["local_points"] , fill="black", font=ImageFont.truetype("arial.ttf", 64))
        draw.text((939,930), scoreboard["visitor_team_short"] , fill="white", font=ImageFont.truetype("arial.ttf", 64))
        draw.text((1124,930), scoreboard["visitor_points"] , fill="black", font=ImageFont.truetype("arial.ttf", 64))
        canvas = canvas.convert('RGB')
        # canvas.save("img.jpeg")
        # Convertir el lienzo a bytes
        # frame_bytes = canvas.tobytes("JPEG")
        buffer = io.BytesIO()
        # imagen.save("test_frame.png")
        canvas.save(buffer, format="JPEG")
        buffer.seek(0)
        # Generar el frame para la fuente de video HTTP
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.read() + b'\r\n')
        end_time = time.time()

        # # Calcular el tiempo transcurrido
        # elapsed_time = end_time - start_time
        # print("Tiempo procesamiento p/frame: " + str(elapsed_time))

def change_video_source(event_id, camera_index):
    redis.set(f'{event_id}-interrupt_flag', int(True))
    redis.set(f'{event_id}-selected_video_soruce', int(camera_index))
    pass