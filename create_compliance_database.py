from compliance.db import populate
from app import create_app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        populate()
