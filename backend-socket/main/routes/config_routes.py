from flask import Blueprint
from flask import render_template
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.services.config_services import  add_video_source, add_socket_video_source, set_yt_rtmp_key, add_new_participant, get_event_participants, join_event, get_some_parameter

config_bp = Blueprint('config', __name__, url_prefix='/config')


@config_bp.route('/add_video_source', methods=['POST'])
@jwt_required(optional=True)
def add_video_source_event():
    data = request.get_json()
    print(data['url'])
    video_source = data['url']
    list_video_sources = add_video_source(video_source)
    return list_video_sources

@config_bp.route('/add_socket_video_source', methods=['POST'])
@jwt_required(optional=False)
def add_socket_video_source_event():
    current_user = get_jwt_identity()
    print(current_user)
    current_user = current_user['user_id']
    list_video_sources = add_socket_video_source(current_user)
    return list_video_sources

@config_bp.route('/set_yt_rtmp_key', methods=['POST'])
@jwt_required(optional=True)
def set_yt_rtmp_key_event():
    data = request.get_json()
    youtube_rtmp_key = data['youtube_rtmp_key']
    return set_yt_rtmp_key(youtube_rtmp_key)

@config_bp.route('/add_new_participant', methods=['POST'])
@jwt_required(optional=True)
def add_new_participant_event():
    data = request.get_json()
    web_url = data['web_url']
    current_user = get_jwt_identity()
    current_user = current_user['user_id']
    return add_new_participant(current_user, web_url)

@config_bp.route('/get_participant_list', methods=['GET'])
@jwt_required(optional=True)
def get_event_participants_event():
    # data = request.get_json()
    current_user = get_jwt_identity()
    current_user = current_user['user_id']
    return get_event_participants(current_user)

@config_bp.route('/join_event/<user_id>', methods=['POST'])
def join_eventevent(user_id):
    return join_event(user_id)

@config_bp.route('/get_parameter/<parameter>', methods=['GET'])
@jwt_required(optional=True)
def get_some_parameter_event(parameter):
    current_user = get_jwt_identity()
    current_user = current_user['user_id']
    return get_some_parameter(current_user, parameter)