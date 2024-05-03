import os
from main import redis
import shortuuid
import cv2
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import ast

from main import sports, sports_name_list
from main.models.event import event
from main.services.scoreboard_services import get_scoreboard



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
    return "done"

#Implementar logica para comenzar stream
def start_event():
    event_id = str(shortuuid.uuid())
    for key in event:
        redis.set(f'{event_id}-{key}', event[key])
    return "done"

def get_sports_list():
    return {int(i): valor for i, valor in enumerate(sports_name_list)}

def generate_frames(event_id):
    video_list = redis.get(f'{event_id}-video_sources')
    bytes_video_list = video_list.decode('utf-8')
    video_list = ast.literal_eval(bytes_video_list)
    capture = cv2.VideoCapture(str(video_list[0]))
    transparent_image = Image.open('sb.png').convert('RGBA')
    alfa = 0
    scoreboard = get_scoreboard(event_id)

    print(os.getpid(), event_id, scoreboard)
    while True:
        scoreboard = get_scoreboard(event_id)
        ret, frame = capture.read()
        # transparent_image.putalpha(int(alfa))
        # if alfa >=255:
        #     alfa = 0
        # alfa += 1
        if not ret:
            continue
        
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

