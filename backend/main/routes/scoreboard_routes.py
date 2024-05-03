from flask import Blueprint
from flask import render_template
from main.services.scoreboard_services import add_point_team, sub_point_team, set_teams, get_scoreboard
from flask import request

scoreboard_bp = Blueprint('scoreboard', __name__, url_prefix='/scoreboard')

@scoreboard_bp.route('/add_point/<team>/<points>/<event_id>', methods=['POST'])
def add_points_event(event_id, team, points):
    team_points = add_point_team(event_id, team, points)
    return  {f'{team}_points' : int(team_points)}

@scoreboard_bp.route('/sub_point/<team>/<points>/<event_id>', methods=['POST'])
def sub_points_event(event_id, team, points):
    team_points = sub_point_team(event_id, team, points)
    return  {f'{team}_points' : int(team_points)}

@scoreboard_bp.route('/set_teams/<event_id>', methods=['POST'])
def set_teams_event(event_id):
    data = request.get_json()
    set_teams(event_id, data)
    return f'Teams setted'

@scoreboard_bp.route('/get/<event_id>', methods=['GET'])
def get_scoreboard_event(event_id):
    return get_scoreboard(event_id)