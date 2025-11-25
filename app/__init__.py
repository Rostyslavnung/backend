import os
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv

from src.User import User

load_dotenv()

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

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
