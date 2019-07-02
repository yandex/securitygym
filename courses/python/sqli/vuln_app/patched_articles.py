from flask import Blueprint
from flask import render_template
from flask import request

from sqli.vuln_app.db import get_db

bp = Blueprint("articles", __name__)


@bp.route("/", methods=("GET", "POST"))
def articles_list():
    db = get_db()
    if request.method == "POST":
        search_title = '%' + request.form['title'] + '%'
        order_by = 'ASC' if request.form['order'] == 'ASC' else 'DESC'
        articles = db.execute("SELECT * FROM article WHERE title LIKE ? ORDER BY created_at %s" % order_by,
                              (search_title,)).fetchall()
    else:
        articles = db.execute("SELECT * FROM article ORDER BY created_at DESC").fetchall()
    return render_template("articles/list.html", articles=articles)
