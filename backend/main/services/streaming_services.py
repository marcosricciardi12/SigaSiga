from main import redis
import shortuuid

event = {
    "sport" : "",
    "video_sources" : str([]),
    "audio_sources" : str([]),
    "start": int(False),
    "play": int(False),
    "stop": int(False),
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

