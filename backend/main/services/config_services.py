from main import redis
import ast

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

def add_video_source(video_source, event_id):
    video_list = redis.get(f'{event_id}_video_sources')
    bytes_video_list = video_list.decode('utf-8')
    video_list = ast.literal_eval(bytes_video_list)
    video_list.append(video_source)
    redis.set(f'{event_id}_video_sources', str(video_list))
    return str(video_list)

def select_sport(sport ,event_id):
    scoreboard = scoreboards[sport]
    redis.set(f'{event_id}_sport', str(sport))
    for key in scoreboard:
        redis.set(f'{event_id}_{key}', scoreboard[key])
    return "done"