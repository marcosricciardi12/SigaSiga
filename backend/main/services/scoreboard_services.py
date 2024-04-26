from main import redis

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

def add_point_team(event_id, team, points):
    team_points = redis.get(f'{event_id}_{team}_points')
    print(redis.get(f'{event_id}_{team}_points'))
    print(f'{event_id}_{team}_points')
    team_points = int(team_points)
    team_points += int(points)
    redis.set(f'{event_id}_{team}_points', team_points)
    return str(team_points)

def sub_point_team(event_id, team, points):
    team_points = redis.get(f'{event_id}_{team}_points')
    print(redis.get(f'{event_id}_{team}_points'))
    print(f'{event_id}_{team}_points')
    team_points = int(team_points)
    team_points -= int(points)
    if team_points < 0: team_points=0
    redis.set(f'{event_id}_{team}_points', team_points)
    return str(team_points)

def set_teams(event_id, teams_data):
    for key in teams_data:
        redis.set(f'{event_id}_{key}', teams_data[key])
    return "done"

def get_scoreboard(event_id):
    deporte = redis.get(f'{event_id}_sport')
    deporte = deporte.decode("utf-8")
    scoreboard = scoreboards[deporte]
    for key in scoreboard:
       scoreboard[key] = redis.get(f'{event_id}_{key}')
    return str(scoreboard)