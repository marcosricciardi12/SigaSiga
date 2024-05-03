from main import redis
from main import sports_name_list
import ast


def add_video_source(video_source, event_id):
    video_list = redis.get(f'{event_id}-video_sources')
    bytes_video_list = video_list.decode('utf-8')
    video_list = ast.literal_eval(bytes_video_list)
    video_list.append(video_source)
    redis.set(f'{event_id}-video_sources', str(video_list))
    return {"video_source_list": video_list}

