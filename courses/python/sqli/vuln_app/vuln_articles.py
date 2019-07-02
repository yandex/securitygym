from flask import Blueprint
from flask import render_template
from flask import request

from sqli.vuln_app.db import get_db

bp = Blueprint("articles", __name__)


@bp.route("/", methods=("GET", "POST"))
def articles_list():
    db = get_db()
    if request.method == "POST":
        search_title = request.form['title']
        order_by = request.form['order']
        articles = db.execute("SELECT * FROM article WHERE title LIKE '%%%s%%' ORDER BY created_at %s"
                              % (search_title, order_by))
    else:
        articles = db.execute("SELECT * FROM article ORDER BY created_at DESC")
    return render_template("articles/list.html", articles=articles)
