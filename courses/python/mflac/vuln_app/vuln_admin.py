from flask import Blueprint
from flask import render_template

from mflac.vuln_app.auth import login_required
from mflac.vuln_app.db import get_db

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/users_list")
@login_required
def users_list():
    db = get_db()
    users = db.execute("SELECT * FROM user").fetchall()
    return render_template('admin/users_list.html', users=users)
