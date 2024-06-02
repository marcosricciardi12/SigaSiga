import base64
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
from main.modules.final_video import generate_final_video
from main.modules.emit_youtube import emit_to_youtube, emit_to_youtube_from_http
import main.modules.remove_redis_data as remove_redis_data
from flask import jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
import uuid
import ast
import multiprocessing as mp


def new_event_service(sport_id):

    wait_image_path = 'main/static/wait.jpg'

# Leer la imagen usando OpenCV
    wait_image = cv2.imread(wait_image_path, cv2.IMREAD_UNCHANGED)
    _, image_encoded = cv2.imencode('.jpeg', wait_image)
    image_bytes = base64.b64encode(image_encoded.tobytes())

    user_id = str(uuid.uuid4())  # Generar un user_id aleatorio
    redis.set(f"user-{user_id}", user_id)
    redis.set(f"user-{user_id}-role", "creator")


    sport_id = int(sport_id)
    selected_sport = sports_name_list[sport_id]
    event_id = str(shortuuid.uuid())
    redis.set(f"user-{user_id}-id_event", event_id)

    sport = sports[sport_id]
    print(sport)
    for key in event:
        redis.set(f'{event_id}-{key}', event[key])
    redis.set(f'{event_id}-event_id', event_id)
    redis.set(f'{event_id}-sport', selected_sport)
    redis.set(f'{event_id}-sport_id', sport_id)
    redis.set(f'{event_id}-creator_user_id', user_id)
    user_identity = {"user_id": user_id}
    access_token = create_access_token(identity=user_identity)
    redis.set(f"user-{user_id}-token", access_token)

    redis.set(f'{event_id}-socket_video_sources-waiting', image_bytes)

    for name_sport in sport:
        # print(name_sport)
        for type_info in sport[name_sport]:
            # print(type_info)
            # print(sport[name_sport][type_info])
            for attribute in sport[name_sport][type_info]:
                # print(attribute)
                redis.set(f'{event_id}-{type_info}-{attribute}', sport[name_sport][type_info][attribute])
    # return read_data_event(event_id)

    final_video_process = mp.Process(target = generate_final_video, args = (redis, event_id))
    final_video_process.start()

    return {"token": access_token, "event_id": event_id}

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
def stop_event():
    current_user = get_jwt_identity()
    current_user = current_user['user_id']
    key = f"user-{current_user}-id_event"
    event_id = (redis.get(key)).decode('utf-8')
    value = int(True)
    redis.set(f'{event_id}-stop', value)
    remove_redis_data.delete_event(event_id, current_user)
    return {f'{event_id} Status': "Stopped and removed"}

#Implementar logica para comenzar stream
def start_event():
    event_id = str(shortuuid.uuid())
    for key in event:
        redis.set(f'{event_id}-{key}', event[key])
    return "done"

def get_sports_list():
    list_dict_deportes = []
    for index, sport in enumerate(sports_name_list):
        list_dict_deportes.append({"id": index, "sport": sport})
    return jsonify({"sports": [sport for sport in list_dict_deportes]})

def generate_frames(current_user):
    
    key = f"user-{current_user}-id_event"
    event_id = (redis.get(key)).decode('utf-8')

    try:
        while not int(redis.get(f'{event_id}-stop')):
            video_frame = redis.get(f'{event_id}-video_frame')
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + video_frame + b'\r\n')
            
    except:
        print("End generate frames")

def change_video_source(event_id, camera_index):
    redis.set(f'{event_id}-interrupt_flag', int(True))
    redis.set(f'{event_id}-selected_video_source', int(camera_index))
    pass

def change_socket_video_source(video_index):
    current_user = get_jwt_identity()
    current_user = current_user['user_id']
    key = f"user-{current_user}-id_event"
    event_id = (redis.get(key)).decode('utf-8')
    redis.set(f'{event_id}-interrupt_flag', int(True))
    redis.set(f'{event_id}-selected_socket_video_source', int(video_index))
    pass

def get_frame_from_redis(key):
    # Obtener el frame almacenado en Redis
    encoded_frame = redis.get(key)
    if encoded_frame is None:
        print("No frame found in Redis for the given key.")
        return None

    # Decodificar el frame de base64
    webp_frame = base64.b64decode(encoded_frame)

    # Convertir los bytes del frame WebP a una matriz de imagen que OpenCV pueda usar
    image_array = np.frombuffer(webp_frame, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    return image

def get_redis_frame(event_id):
    video_source_index = int(redis.get(f'{event_id}-selected_socket_video_source'))
    video_list = redis.get(f'{event_id}-socket_video_sources')
    bytes_video_list = video_list.decode('utf-8')
    video_list = ast.literal_eval(bytes_video_list)
    print(video_list)
    key_user_video_source = str(video_list[video_source_index])
    key_video_source = f'{event_id}-socket_video_sources-{key_user_video_source}'
    print("hola", key_video_source)
    transparent_image = Image.open('sb.png').convert('RGBA')
    alfa = 0
    scoreboard = get_scoreboard(event_id)
    # capture = capture_list[0]
    print(os.getpid(), event_id, scoreboard)
    while not int(redis.get(f'{event_id}-stop')):
        # start_time = time.time()
        if int(redis.get(f'{event_id}-interrupt_flag')):
            redis.set(f'{event_id}-interrupt_flag', int(False))
            video_source_index = int(redis.get(f'{event_id}-selected_socket_video_source'))
            video_list = redis.get(f'{event_id}-socket_video_sources')
            bytes_video_list = video_list.decode('utf-8')
            video_list = ast.literal_eval(bytes_video_list)
            key_user_video_source = str(video_list[video_source_index])
            key_video_source = f'{event_id}-socket_video_sources-{key_user_video_source}'
            print(video_source_index)

        # frame_bytes = redis.get(key_video_source)
        # # if frame_bytes:
        # #     # Convertir los bytes del frame a formato de imagen
        # nparr = np.frombuffer(frame_bytes, np.uint8)
        # frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        frame = get_frame_from_redis(key_video_source)
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
        video_frame = buffer.read()
        redis.set(f'{event_id}-video_frame', video_frame)
        # Generar el frame para la fuente de video HTTP
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + video_frame + b'\r\n')
        end_time = time.time()

def start_youtube_streaming():
    current_user = get_jwt_identity()
    current_user = current_user['user_id']
    key = f"user-{current_user}-id_event"
    event_id = (redis.get(key)).decode('utf-8')
    value = int(True)
    if not int(redis.get(f'{event_id}-youtube_streaming_status')):
        redis.set(f'{event_id}-youtube_streaming_status', value)
        emit_to_youtube_process = mp.Process(target = emit_to_youtube, args = (redis, event_id))
        emit_to_youtube_process.start()
        return {f'{event_id} Youtube Streaming Status': "Streaming started"}
    return {f'{event_id} Youtube Streaming Status': "Event is already Streaming on youtube"}

def stop_youtube_streaming():
    current_user = get_jwt_identity()
    current_user = current_user['user_id']
    key = f"user-{current_user}-id_event"
    event_id = (redis.get(key)).decode('utf-8')
    value = int(False)
    redis.set(f'{event_id}-youtube_streaming_status', value)
    return {f'{event_id} Youtube Streaming Status': "Streaming Stopped"}

def start_youtube_streaming2(token):
    print(token)
    current_user = get_jwt_identity()
    current_user = current_user['user_id']
    key = f"user-{current_user}-id_event"
    event_id = (redis.get(key)).decode('utf-8')
    value = int(True)
    if not int(redis.get(f'{event_id}-youtube_streaming_status')):
        redis.set(f'{event_id}-youtube_streaming_status', value)
        emit_to_youtube_process = mp.Process(target = emit_to_youtube_from_http, args = (token, redis, event_id))
        emit_to_youtube_process.start()
        return {f'{event_id} Youtube Streaming Status': "Streaming started"}
    return {f'{event_id} Youtube Streaming Status': "Event is already Streaming on youtube"}
