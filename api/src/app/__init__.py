from flask import Flask

from app import settings
from app import auth
from app import courses
from app import db


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False

    app.config.from_mapping(
        SECRET_KEY = settings.SECRET_KEY
    )

    app.register_blueprint(auth.bp)
    app.register_blueprint(courses.bp)

    with app.app_context():
        db.init_db()

    return app
