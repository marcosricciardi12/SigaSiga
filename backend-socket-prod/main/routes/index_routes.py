from flask import Blueprint
from flask import render_template
from flask import request

from main.services.config_services import  add_video_source

index_bp = Blueprint('index', __name__, url_prefix='/index')


@index_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')