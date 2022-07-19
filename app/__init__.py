# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__version__ = "0.1.0"

# Import core packages
import os

# Import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.views import refget_blueprint
from .models import db

migrate = Migrate()


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

    cors_cfg = app.config["CORS"]
    CORS(
        app=app,
        methods=cors_cfg["METHODS"],
        allow_headers=cors_cfg["ALLOW_HEADERS"],
        expose_headers=cors_cfg["EXPOSE_HEADERS"],
        max_age=cors_cfg["MAX_AGE"],
    )

    db.init_app(app)
    migrate.init_app(app, db, "migrations")
    return app
