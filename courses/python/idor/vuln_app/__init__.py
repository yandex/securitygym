from flask import Flask
import uuid


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY=str(uuid.uuid4()),
        DATABASE="payments.sqlite",
        VULNERABLE=True
    )

    if test_config is not None:
        app.config.update(test_config)

    with app.app_context():
        from idor.vuln_app import db
        db.init_db()
        import idor.vuln_app.vuln_payments

    from idor.vuln_app import auth
    app.register_blueprint(auth.bp)
    if app.config["VULNERABLE"]:
        import idor.vuln_app.vuln_payments as payments
    else:
        import idor.vuln_app.patched_payments as payments
    app.register_blueprint(payments.bp)

    return app
