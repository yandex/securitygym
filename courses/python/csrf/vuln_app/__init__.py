from flask import Flask
from flask_wtf import CSRFProtect
import uuid


csrf_protection = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_mapping(
        SECRET_KEY=str(uuid.uuid4()),
        DATABASE="payments.sqlite",
        VULNERABLE=True
    )

    csrf_protection.init_app(app)

    if test_config is not None:
        app.config.update(test_config)

    with app.app_context():
        from csrf.vuln_app import db
        db.init_db()

    from csrf.vuln_app import auth
    csrf_protection.exempt(auth.bp)
    app.register_blueprint(auth.bp)
    if app.config["VULNERABLE"]:
        import csrf.vuln_app.vuln_payments as payments
    else:
        import csrf.vuln_app.patched_payments as payments
    app.register_blueprint(payments.bp)

    return app
