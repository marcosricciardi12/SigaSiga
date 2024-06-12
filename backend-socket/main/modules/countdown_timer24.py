import os
import time
from main import redis

def countdown_timer24(event_id):
    try:
        print(f'{event_id} 24timer started')
        while True and not int(redis.get(f'{event_id}-stop')):
            play_time = int(redis.get(f"{event_id}-scoreboard-play_24time").decode("utf-8"))
            current_time = int(redis.get(f"{event_id}-scoreboard-24time").decode("utf-8"))
            if play_time and current_time>0:
                time.sleep(0.1)
                current_time -= 100
                if current_time<=0: 
                    current_time=0
                    redis.set(f'{event_id}-scoreboard-play_24time', int(False))
                redis.set(f"{event_id}-scoreboard-24time", current_time)
        os._exit(0)
    except:
        print("24Timer closed")
        os._exit(0)