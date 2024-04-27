import os
from main import redis
import shortuuid
import cv2
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import ast

event = {
    "sport" : "",
    "video_sources" : str([]),
    "audio_sources" : str([]),
    "start": int(False),
    "play": int(False),
    "stop": int(False),
}

scoreboards = {
    "basquet": {
        "local_team": "",
        "local_team_short": "",
        "local_points": 0,
        "local_fouls": 0,
        "visitor_team": "",
        "visitor_team_short": "",
        "visitor_points": 0,
        "visitor_fouls": 0,
        "period": 0,
        "time": 0,
        "24time": 0,
        "play_time": int(False),
        "play_24time": int(False)
    }
}

def new_event_service():
    event_id = str(shortuuid.uuid())
    for key in event:
        redis.set(f'{event_id}_{key}', event[key])
    return event_id

def read_data_event(event_id):
    for key in event:
        event[key] = redis.get(f'{event_id}_{key}')
    return event

def play_event(event_id):
    value = int(True)
    redis.set(f'{event_id}_play', value)
    return "done"

def pause_event(event_id):
    value = int(False)
    redis.set(f'{event_id}_play', value)
    return "done"

#cambio stop a True, matara al streaming
def stop_event(event_id):
    value = int(True)
    redis.set(f'{event_id}_stop', value)
    return "done"

#Implementar logica para comenzar stream
def start_event():
    event_id = str(shortuuid.uuid())
    for key in event:
        redis.set(f'{event_id}_{key}', event[key])
    return "done"

def get_scoreboard(event_id):
    deporte = redis.get(f'{event_id}_sport')
    deporte = deporte.decode("utf-8")
    scoreboard = scoreboards[deporte]
    for key in scoreboard:
       scoreboard[key] = redis.get(f'{event_id}_{key}').decode("utf-8")
    return scoreboard

def generate_frames(event_id):
    video_list = redis.get(f'{event_id}_video_sources')
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

