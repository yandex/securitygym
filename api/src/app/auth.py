from flask import Blueprint
from flask import request
from flask import jsonify
from flask import session
from flask import g
from flask import abort
import functools
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from app.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return abort(403)
        return view(**kwargs)
    return wrapped_view


@bp.before_app_request
def load_logged_user():
    uid = session.get("uid")

    if uid is None:
        g.user = None
    else:
        cursor = get_db().cursor()
        cursor.execute("SELECT uid, username FROM users WHERE uid = %s", (uid,))
        user = cursor.fetchone()
        g.user = {
            "uid": user[0],
            "username": user[1]
        }


@bp.route("/register", methods=("POST",))
def register():
    if request.method == "POST":
        r = request.json
        username = r["username"]
        password = r["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username required"
        elif not password:
            error = "Password required"
        else:
            cursor = db.cursor()
            cursor.execute("SELECT uid FROM users WHERE username = %s", (username,))
            if cursor.fetchone() is not None:
                error = "User {0} is already registered".format(username)

        if error is None:
            db.cursor().execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                           (username, generate_password_hash(password)))
            db.commit()
            return jsonify({"status": "OK"}), 200

        return jsonify({"status": "ERROR", "error": error}), 400


@bp.route("/login", methods=("POST",))
def login():
    if request.method == "POST":
        r = request.json
        username = r["username"]
        password = r["password"]
        db = get_db()
        error = None
        cursor = db.cursor()
        cursor.execute("SELECT uid, username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user is None or not check_password_hash(user[2], password):
            error = "Incorrect username or password"

        if error is None:
            session.clear()
            session["uid"] = user[0]
            return jsonify({"status": "OK"}), 200

    return jsonify({"status": "ERROR", "error": error}), 403


@bp.route("/logout")
def logout():
    session.clear()
    return jsonify({"status": "OK"})


@bp.route("/username")
@login_required
def get_username():
    return jsonify({"username": g.user["username"], "uid": g.user["uid"]})
