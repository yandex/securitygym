from flask import Blueprint
from flask import g
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template

import functools

from idor.vuln_app.db import get_db

bp = Blueprint("payments", __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view


@bp.route("/")
@login_required
def user_payments():
    db = get_db()
    payments = db.execute("SELECT * FROM payment WHERE user_id = ? ORDER BY id",
                          (g.user["id"],)).fetchall()
    return render_template("payments/payments_list.html", payments=payments)


@bp.route("/payment/<int:payment_id>")
@login_required
def view_payment(payment_id):
    db = get_db()
    payment = db.execute("SELECT * FROM payment WHERE id = ?", (payment_id,)).fetchone()
    return render_template("payments/payment_details.html", payment=payment)


@bp.route("/add_payment", methods=("GET", "POST"))
@login_required
def add_payment():
    if request.method == "POST":
        db = get_db()
        amount = request.form["amount"]
        description = request.form["description"]
        error = None

        if not amount:
            error = "Amount required"
        if not description:
            error = "Description required"

        if error is None:
            db.execute("INSERT INTO payment (user_id, amount, description) VALUES (?, ?, ?)",
                       (g.user["id"], amount, description)
                       )
            db.commit()
            return redirect(url_for("payments.user_payments"))

    return render_template("payments/add_payment.html")
