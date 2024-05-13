from main import redis as redis_db

def generate_video_source(event_id, video_source_index):
    key_video_source = f'{event_id}-video_sources-{str(video_source_index)}'
    while not int(redis_db.get(f'{event_id}-stop')):
        frame_bytes = redis_db.get(key_video_source)
        if frame_bytes:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')