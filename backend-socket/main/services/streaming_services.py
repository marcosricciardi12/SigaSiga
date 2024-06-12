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
from main.modules.countdown_timer import countdown_timer
from main.modules.countdown_timer24 import countdown_timer24
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
    image_bytes = image_encoded.tobytes()

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

    timer_process = mp.Process(target = countdown_timer, args= (event_id,))
    timer_process.start()

    timer24_process = mp.Process(target = countdown_timer24, args= (event_id,))
    timer24_process.start()
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

def generate_http_frames_final_video(current_user):
    
    key = f"user-{current_user}-id_event"
    event_id = (redis.get(key)).decode('utf-8')

    try:
        while not int(redis.get(f'{event_id}-stop')):
            time.sleep(1/33)
            video_frame = redis.get(f'{event_id}-video_frame')
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + video_frame + b'\r\n')
            
    except Exception as e:
        print("End generate frames: ", e)

def generate_http_frames_source_video(current_user, source_id):

    event_id_key = f"user-{current_user}-id_event"
    event_id = (redis.get(event_id_key)).decode('utf-8')

    video_source_key = f'{event_id}-socket_video_sources-{source_id}'
    print(video_source_key)
    try:
        while not int(redis.get(f'{event_id}-stop')):
            time.sleep(1/33)
            video_frame = redis.get(video_source_key)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + video_frame + b'\r\n')
            
    except Exception as e:
        print("End generate frames: ", e)

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
