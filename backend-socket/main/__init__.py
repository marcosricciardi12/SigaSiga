from flask import Flask
from main.config import Config
from redis import Redis
from main.starts.load_sports import load_sports
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt_identity

redis = Redis()
sports, sports_name_list = load_sports()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.redis = redis

    app.config['JWT_SECRET_KEY'] = "asfgakdfjsdkfhkas"#os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 14400 #int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)
    
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
