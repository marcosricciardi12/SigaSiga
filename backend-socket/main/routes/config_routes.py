from flask import Blueprint
from flask import render_template
from flask import request

from main.services.config_services import  add_video_source

config_bp = Blueprint('config', __name__, url_prefix='/config')


@config_bp.route('/add_video_source/<event_id>', methods=['POST'])
def add_video_source_event(event_id):
    data = request.get_json()
    print(data['url'])
    video_source = data['url']
    list_video_sources = add_video_source(video_source, event_id)
    return list_video_sources