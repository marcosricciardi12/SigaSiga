from flask import Blueprint, Response, request, jsonify
from flask import render_template
from main.services.streaming_services import ( new_event_service, read_data_event , 
                                              play_event , pause_event, get_sports_list,
                                              stop_event, change_video_source, generate_frames,
                                              change_socket_video_source, get_redis_frame,
                                              start_youtube_streaming, stop_youtube_streaming)
                                              
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_header, decode_token
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            decoded_token = decode_token(token)
            print(decoded_token)
            request.user_identity = decoded_token['sub']['user_id']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated_function

streaming_bp = Blueprint('streaming', __name__, url_prefix='/streaming')

@streaming_bp.route('/new_event/<sport_id>', methods=['POST'])
def new_event(sport_id):
    event_id = new_event_service(sport_id)
    return event_id

#Devuelve un diccionario que contiene como clave/valor el indice correspondiente al nombre del deporte en la lista de los deportes disponibles.
@streaming_bp.route('/get_sports', methods=['GET'])
def get_sports():
    data = get_sports_list()
    return data

@streaming_bp.route('/data_event/<event_id>', methods=['GET'])
def data_event(event_id):
    data = read_data_event(event_id)
    return data

@streaming_bp.route('/play_event/<event_id>', methods=['POST'])
def play(event_id):
    play_event(event_id)
    return 'Streaming playing'

@streaming_bp.route('/pause_event/<event_id>', methods=['POST'])
def pause(event_id):
    pause_event(event_id)
    return 'Streaming paused'


@streaming_bp.route('/stop_event', methods=['POST'])
@jwt_required(optional=True)
def stop():
    return stop_event()


@streaming_bp.route('/video_feed/', methods=['GET'])
@token_required
def video_feed():
    current_user = request.user_identity 
    print(current_user)
    return Response(generate_frames(current_user), mimetype='multipart/x-mixed-replace; boundary=frame')

@streaming_bp.route('/video_feed/<event_id>', methods=['GET'])
def video_feed_event(event_id):
    return Response(get_redis_frame(event_id), mimetype='multipart/x-mixed-replace; boundary=frame')


@streaming_bp.route('/change_video_source/<event_id>/<camera_index>', methods=['POST'])
@jwt_required(optional=True)
def change_video_source_event(event_id, camera_index):
    change_video_source(event_id, camera_index)
    return f'Teams setted'

@streaming_bp.route('/change_socket_video_source/', methods=['POST'])
@jwt_required(optional=True)
def change_socket_video_source_event():
    change_socket_video_source()
    return f'Video Source Changed'

@streaming_bp.route('/start_youtube_streaming', methods=['POST'])
@jwt_required(optional=True)
def start_youtube_streaming_event():
    return start_youtube_streaming()

@streaming_bp.route('/stop_youtube_streaming', methods=['POST'])
@jwt_required(optional=True)
def stop_youtube_streaming_event():
    return stop_youtube_streaming()