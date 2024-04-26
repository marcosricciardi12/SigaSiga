from flask import Flask
from main.config import Config
from redis import Redis

redis = Redis()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.redis = redis
    from main.routes.config_routes import config_bp
    from main.routes.scoreboard_routes import scoreboard_bp
    from main.routes.streaming_routes import streaming_bp

    app.register_blueprint(config_bp)
    app.register_blueprint(scoreboard_bp)
    app.register_blueprint(streaming_bp)

    return app
