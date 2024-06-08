from flask import Blueprint, Response, request, jsonify
from flask import render_template
from main.services.streaming_services import ( new_event_service, read_data_event , 
                                              play_event , pause_event, get_sports_list,
                                              stop_event, change_video_source, generate_http_frames_final_video,
                                              change_socket_video_source, generate_http_frames_source_video,
                                              start_youtube_streaming2, stop_youtube_streaming)
                                              
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
    return Response(generate_http_frames_final_video(current_user), mimetype='multipart/x-mixed-replace; boundary=frame')


@streaming_bp.route('/video_feed_source/<source_id>', methods=['GET'])
@token_required
def video_feed_event(source_id):
    current_user = request.user_identity 
    return Response(generate_http_frames_source_video(current_user, source_id), mimetype='multipart/x-mixed-replace; boundary=frame')


@streaming_bp.route('/change_video_source/<event_id>/<camera_index>', methods=['POST'])
@jwt_required(optional=True)
def change_video_source_event(event_id, camera_index):
    change_video_source(event_id, camera_index)
    return f'Teams setted'

@streaming_bp.route('/change_socket_video_source/<video_source_index>', methods=['POST'])
@jwt_required(optional=True)
def change_socket_video_source_event(video_source_index):
    change_socket_video_source(video_source_index)
    return f'Video Source Changed'

@streaming_bp.route('/start_youtube_streaming', methods=['POST'])
@jwt_required(optional=True)
def start_youtube_streaming_event():
    token = request.headers.get('Authorization').split()[1]
    return start_youtube_streaming2(token)

@streaming_bp.route('/stop_youtube_streaming', methods=['POST'])
@jwt_required(optional=True)
def stop_youtube_streaming_event():
    return stop_youtube_streaming()