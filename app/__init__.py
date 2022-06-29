__version__ = "0.1.0"

# Import core packages
import os

# Import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.views import refget_blueprint
from .models import db


def create_app(config=None):
    # Inject Flask magic
    app = Flask(__name__)
    app.register_blueprint(refget_blueprint)

    # Load configuration
    app.config.from_object("app.config.Config")
    if os.environ.get("REFGET_SETTINGS"):
        app.config.from_envvar("REFGET_SETTINGS", silent=False)
    if config is not None:
        app.config.from_object(config)

    db.init_app(app)
    return app
