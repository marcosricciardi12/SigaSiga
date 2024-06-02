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