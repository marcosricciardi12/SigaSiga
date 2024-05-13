from flask import Flask
from main.config import Config
from redis import Redis
from main.starts.load_sports import load_sports
from flask_cors import CORS


redis = Redis()
sports, sports_name_list = load_sports()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.redis = redis

    from main.routes.config_routes import config_bp
    from main.routes.scoreboard_routes import scoreboard_bp
    from main.routes.streaming_routes import streaming_bp
    from main.routes.video_sources_routes import video_source_bp
    from main.routes.index_routes import index_bp
    
    app.register_blueprint(config_bp)
    app.register_blueprint(scoreboard_bp)
    app.register_blueprint(streaming_bp)
    app.register_blueprint(video_source_bp)
    app.register_blueprint(index_bp)

    from main.sockets.sockets import socketio

    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")

    return app, socketio
