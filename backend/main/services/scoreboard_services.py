from main import redis
from main import sports, sports_name_list


def add_point_team(event_id, team, points):
    team_points = redis.get(f'{event_id}-scoreboard-{team}_points')
    team_points = int(team_points)
    team_points += int(points)
    if team_points < 0 : team_points = 0
    redis.set(f'{event_id}-scoreboard-{team}_points', team_points)
    return str(team_points)

def sub_point_team(event_id, team, points):
    team_points = redis.get(f'{event_id}-scoreboard-{team}_points')
    team_points = int(team_points)
    team_points -= int(points)
    if team_points < 0 : team_points = 0
    redis.set(f'{event_id}-scoreboard-{team}_points', team_points)
    return str(team_points)

def set_teams(event_id, teams_data):
    for key in teams_data:
        redis.set(f'{event_id}-scoreboard-{key}', teams_data[key])
    return "done"

def get_scoreboard(event_id):
    sport_id = int(redis.get(f'{event_id}-sport_id'))
    sport_name = sports_name_list[sport_id]
    sport = sports[sport_id]
    scoreboard = sport[sport_name]["scoreboard"]
    # print(scoreboard)
    for attribute in scoreboard:
    #    print(attribute)
       scoreboard[attribute] = redis.get(f'{event_id}-scoreboard-{attribute}').decode("utf-8")
    return scoreboard