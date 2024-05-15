from main import redis
from main import sports_name_list
import ast
from main.modules.capture_http_video_redis import capture_video_source
import multiprocessing as mp

def add_video_source(video_source, event_id):
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

