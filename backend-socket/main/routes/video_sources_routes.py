from flask import Blueprint, Response, request
from flask import render_template
from main.services.video_sources_services import generate_video_source

video_source_bp = Blueprint('video_source', __name__, url_prefix='/video_feed/source')

@video_source_bp.route('/<event_id>/<video_source_index>', methods=['GET'])
def generate_video(event_id, video_source_index):
    return Response(generate_video_source(event_id, video_source_index), mimetype='multipart/x-mixed-replace; boundary=frame')