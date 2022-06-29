__version__ = "0.1.0"

# Import core packages
import os

# Import Flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Inject Flask magic
app = Flask(__name__)

# Load configuration
app.config.from_object("app.config.Config")
if os.environ.get("REFGET_SETTINGS"):
    app.config.from_envvar("REFGET_SETTINGS", silent=False)

# Construct the DB Object (SQLAlchemy interface)
db = SQLAlchemy(app)

# Enabel migration for our application
# Migrate(app, db)

# Import routing to render the pages
from app import views, models
