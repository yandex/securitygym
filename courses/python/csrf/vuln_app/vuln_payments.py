from flask import Blueprint
from flask import g
from flask import render_template
from flask import render_template_string
from flask import request
from flask import redirect
from flask import flash

from csrf.vuln_app.auth import login_required
from csrf.vuln_app.db import get_db
from csrf.vuln_app import csrf_protection

bp = Blueprint("payments", __name__)


@bp.route("/")
@login_required
def user_payments():
    db = get_db()
    payments = db.execute("SELECT p.id, p.amount, p.created_at, u_from.username as from_username, "
                            "u_to.username as to_username "
                          "FROM payment as p "
                          "JOIN user as u_from ON p.from_user_id = u_from.id "
                          "JOIN user as u_to ON p.to_user_id = u_to.id "
                          "WHERE p.from_user_id = ? OR p.to_user_id = ? "
                          "ORDER BY created_at DESC",
                          (g.user["id"], g.user["id"])).fetchall()
    return render_template("payments/payments_list.html", payments=payments, balance=g.user["balance"])


@bp.route("/send", methods=("GET", "POST"))
@login_required
@csrf_protection.exempt
def send():
    db = get_db()
    if request.method == "POST":
        amount = int(request.form["amount"])
        if g.user["balance"] < amount:
            flash("Not enough money on balance")
            return redirect("/")
        if amount <= 0:
            flash("You can not transfer a negative amount")
            return redirect("/send")
        to_user_id = request.form["to_user_id"]
        if to_user_id == g.user["id"]:
            flash("You cannot send payment to yourself")
            return redirect("/send")
        db.execute("UPDATE user SET balance = balance - ? WHERE id = ?", (amount, g.user["id"]))
        db.execute("UPDATE user SET balance = balance + ? WHERE id = ?", (amount, to_user_id))
        db.execute("INSERT INTO payment (from_user_id, to_user_id, amount, created_at) "
                   "VALUES (?, ?, ?, date('now'))", (g.user["id"], to_user_id, amount))
        db.commit()
        return redirect("/")
    users = db.execute("SELECT id, username FROM user WHERE id <> ?", (g.user["id"],)).fetchall()
    return render_template_string('''
    {% extends 'base.html' %}

    {% block header %}
        <h1>{% block title %}Send Money{% endblock %}</h1>
    {% endblock %}
    
    {% block content %}
        <form method="post">
            <label for="amount">Amount</label>
            <input type="number" name="amount" id="amount" value="0" step="0.01" required>
            <label for="to_user_id">To user</label>
            <select name="to_user_id" id="to_user_id">
                {% for user in users %}
                <option value="{{ user.id }}">{{ user.username }}</option>
                {% endfor %}
            </select>
            <input type="submit" value="Add payment">
        </form>
    {% endblock %}
    ''', users=users)
