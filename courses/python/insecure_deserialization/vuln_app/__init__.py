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
        import insecure_deserialization.vuln_app.vuln_config as config
    else:
        import insecure_deserialization.vuln_app.patched_config as config
    app.register_blueprint(config.bp)

    return app
