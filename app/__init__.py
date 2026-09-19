"""Application factory for the weather assistant."""
from flask import Flask

from config import Config


def create_app(config_object=Config):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config_object)

    from app.routes import weather_bp

    app.register_blueprint(weather_bp)
    return app
