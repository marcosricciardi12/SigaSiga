from flask import Blueprint, Response, request
from flask import render_template
from main.services.streaming_services import ( new_event_service, read_data_event , 
                                              play_event , pause_event, get_sports_list,
                                              stop_event, change_video_source, generate_frames)

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

@streaming_bp.route('/stop_event/<event_id>', methods=['POST'])
def stop(event_id):
    return stop_event(event_id)


@streaming_bp.route('/video_feed/<event_id>', methods=['GET'])
def video_feed(event_id):
    return Response(generate_frames(event_id), mimetype='multipart/x-mixed-replace; boundary=frame')

@streaming_bp.route('/change_video_source/<event_id>/<camera_index>', methods=['POST'])
def change_video_source_event(event_id, camera_index):
    change_video_source(event_id, camera_index)
    return f'Teams setted'