from flask import Flask
import uuid


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY=str(uuid.uuid4()),
        VULNERABLE=True
    )

    if test_config is not None:
        app.config.update(test_config)

    if app.config["VULNERABLE"]:
        import ssti.vuln_app.vuln_badge_generator as badge_generator
    else:
        import ssti.vuln_app.patched_badge_generator as badge_generator
    app.register_blueprint(badge_generator.bp)

    return app
