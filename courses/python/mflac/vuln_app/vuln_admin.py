from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import g

import functools

from mflac.vuln_app.db import get_db

bp = Blueprint("admin", __name__, url_prefix="/admin")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


@bp.route("/users_list")
@login_required
def users_list():
    db = get_db()
    users = db.execute("SELECT id, username, is_admin FROM user").fetchall()
    return render_template('admin/users_list.html', users=users)
