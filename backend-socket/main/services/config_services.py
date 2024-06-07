from base64 import encodebytes
from io import BytesIO
import uuid
import qrcode
from flask import jsonify, send_file
from main import redis
from main import sports_name_list
import ast
from main.modules.capture_http_video_redis import capture_video_source
import multiprocessing as mp
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

def add_video_source(video_source, event_id):
    current_user = get_jwt_identity()
    current_user = current_user['user_id']
    event_id = redis.get(f"user-{current_user}-id_event")
    event_id = event_id.decode('utf-8')
    video_list = redis.get(f'{event_id}-video_sources')
    bytes_video_list = video_list.decode('utf-8')
    video_list = ast.literal_eval(bytes_video_list)
    video_list.append(video_source)
    video_index = len(video_list) - 1
    redis.set(f'{event_id}-video_sources', str(video_list))
    video_source_key = f'{event_id}-video_sources-{str(video_index)}'
    print(video_source_key)
    video_capture_process = mp.Process(target = capture_video_source, args = (redis, video_source_key, video_source, event_id))
    video_capture_process.start()
    return {"video_source_list": video_list}


def add_socket_video_source(current_user):
    
    event_id = redis.get(f"user-{current_user}-id_event")
    event_id = event_id.decode('utf-8')
    video_list = redis.get(f'{event_id}-socket_video_sources')
    if video_list:
        bytes_video_list = video_list.decode('utf-8')
        video_list = ast.literal_eval(bytes_video_list)
    else:
        video_list = []
    video_list.append(current_user)
    redis.set(f'{event_id}-socket_video_sources', str(video_list))
    video_source_key = f'{event_id}-socket_video_sources-{str(current_user)}'
    print(video_source_key)
    return {"video_source_list": video_list}

def set_yt_rtmp_key(yt_rtmp_key):
    current_user = get_jwt_identity()
    current_user = current_user['user_id']
    event_id = redis.get(f"user-{current_user}-id_event")
    print(event_id)
    event_id = event_id.decode('utf-8')
    redis.set(f'{event_id}-youtube_rtmp_key', str(yt_rtmp_key))
    return {"youtube-rtmp-key": "Saved"}

def add_new_participant(current_user, web_url):
    print(current_user)
    event_id = redis.get(f"user-{current_user}-id_event")
    event_id = event_id.decode('utf-8')
    request_role = redis.get(f"user-{current_user}-role").decode('utf-8')
    participant_role = "participant"
    if request_role == 'creator':
        new_user_id = str(uuid.uuid4())  # Generar un new_user_id aleatorio
        redis.set(f"user-{new_user_id}", new_user_id)
        redis.set(f"user-{new_user_id}-role", participant_role)
        redis.set(f"user-{new_user_id}-id_event", event_id)
        new_user_identity = {"user_id": new_user_id}
        access_token = create_access_token(identity=new_user_identity)
        redis.set(f"user-{new_user_id}-token", access_token)    
        redis.set(f"{event_id}-participant-{new_user_id}", new_user_id)

        join_url = web_url + f'/join-event?user_id={str(new_user_id)}'
        redis.set(f"user-{new_user_id}-join_url", join_url)   

        join_qr_img = qr_generate(join_url)
        redis.set(f"user-{new_user_id}-join_qr_img", join_qr_img)

        return {"token": access_token, "event_id": event_id, "role": participant_role, "user_id": new_user_id, "join_url": join_url, "join_qr_img": join_qr_img} 
    
    return {"error": "Este usuario no puede modificar participantes"}


def get_event_participant(user_id):

    redis.set(f"user-{user_id}", user_id)
    participant_role = redis.get(f"user-{user_id}-role").decode('utf-8')
    event_id = redis.get(f"user-{user_id}-id_event").decode('utf-8')
    access_token = redis.get(f"user-{user_id}-token").decode('utf-8')
    join_url = redis.get(f"user-{user_id}-join_url").decode('utf-8')
    join_qr_img = redis.get(f"user-{user_id}-join_qr_img").decode('utf-8')

    return {"token": access_token, "event_id": event_id, "role": participant_role, "user_id": user_id, "join_url": join_url, "join_qr_img": join_qr_img} 
    
def get_event_participants(current_user):
    event_id = redis.get(f"user-{current_user}-id_event")
    event_id = event_id.decode('utf-8')
    pattern = f"{event_id}-participant-*"
    list_keys = scan_keys(pattern)
    keys_dict = {"participants": [redis.get(key.decode('utf-8')).decode('utf-8') for key in list_keys]}
    return jsonify(keys_dict)

def scan_keys(pattern):
    print(pattern)
    cursor = '0'
    keys = []
    while cursor != 0:
        cursor, batch_keys = redis.scan(cursor=cursor, match=pattern)
        keys.extend(batch_keys)
    print(keys)
    return keys

def join_event(participant_user_id):
    access_token = redis.get(f"user-{participant_user_id}-token").decode('utf-8')
    event_id = redis.get(f"user-{participant_user_id}-id_event").decode('utf-8')
    return {"token": access_token, "event_id": event_id}

def get_some_parameter(current_user, parameter):
    try:
        event_id = redis.get(f"user-{current_user}-id_event")
        event_id = event_id.decode('utf-8')
        pattern = f"{event_id}-{parameter}"
        print(pattern)
        result = redis.get(pattern).decode('utf-8')
        print(result)
        return {f"{parameter}": str(result)}
    except Exception as e:
        print(e)
        return {f"{parameter}": "", "error": "error al obtener el parametro"}
    

def qr_generate(join_url):
    buffer = BytesIO()
    data = str(join_url)

    img = qrcode.make(data)
    img.save(buffer)
    buffer.seek(0)
    send_file(buffer, mimetype='image/png')
    encoded_img_qr = encodebytes(buffer.getvalue()).decode('ascii')
    return encoded_img_qr