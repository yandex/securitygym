from flask import Flask
import uuid


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY=str(uuid.uuid4()),
        DATABASE="articles.sqlite",
        VULNERABLE=True
    )

    if test_config is not None:
        app.config.update(test_config)

    with app.app_context():
        from sqli.vuln_app import db
        db.init_db()

    if app.config["VULNERABLE"]:
        import sqli.vuln_app.vuln_articles as articles
    else:
        import sqli.vuln_app.patched_articles as articles
    app.register_blueprint(articles.bp)

    return app
