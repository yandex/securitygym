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
        import xxe.vuln_app.vuln_bill as bill
    else:
        import xxe.vuln_app.patched_bill as bill
    app.register_blueprint(bill.bp)

    return app
