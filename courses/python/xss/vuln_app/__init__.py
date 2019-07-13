from flask import Flask
import uuid


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY=str(uuid.uuid4()),
        DATABASE="guestbook.sqlite",
        VULNERABLE=True
    )

    if test_config is not None:
        app.config.update(test_config)

    with app.app_context():
        from xss.vuln_app import db
        db.init_db()

    if app.config["VULNERABLE"]:
        import xss.vuln_app.vuln_guestbook as guestbook
    else:
        import xss.vuln_app.patched_guestbook as guestbook
    app.register_blueprint(guestbook.bp)

    return app
