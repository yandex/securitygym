from flask import Flask
import uuid


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY=str(uuid.uuid4()),
        DATABASE="users.sqlite",
        VULNERABLE=True
    )

    if test_config is not None:
        app.config.update(test_config)

    with app.app_context():
        from mflac.vuln_app import db
        db.init_db()

    from mflac.vuln_app import auth
    app.register_blueprint(auth.bp)
    from mflac.vuln_app import index
    app.register_blueprint(index.bp)
    if app.config["VULNERABLE"]:
        import mflac.vuln_app.vuln_admin as admin
    else:
        import mflac.vuln_app.patched_admin as admin
    app.register_blueprint(admin.bp)

    return app
