from flask import Flask
from flask_login import LoginManager
from flask_session import Session
import redis

from app.src import User
from config import Config
from database import init_db

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)

    if app.config.get("SESSION_TYPE") == "redis":
        app.config["SESSION_REDIS"] = redis.from_url(app.config["REDIS_URL"])
        Session(app)
        
    with app.app_context():
        init_db()

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)
    
    from routes.kettles import kettles_bp
    from routes.types import types_bp
    from routes.colors import colors_bp
    from routes.materials import materials_bp
    from routes.producers import producers_bp
    from routes.auth import auth_bp
    from api.api import api

    app.register_blueprint(kettles_bp)
    app.register_blueprint(types_bp)
    app.register_blueprint(colors_bp)
    app.register_blueprint(materials_bp)
    app.register_blueprint(producers_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api, url_prefix="/api")

    return app
