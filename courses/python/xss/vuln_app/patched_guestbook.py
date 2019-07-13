from flask import Blueprint
from flask import render_template_string
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import escape

import re

from xss.vuln_app.db import get_db

bp = Blueprint("guestbook", __name__)


@bp.route("/")
def index():
    db = get_db()
    messages = db.execute("SELECT message, created_at FROM messages ORDER BY created_at DESC").fetchall()
    messages_for_render = []
    current_number = len(messages)
    replace_str = re.compile("(guestbook)", re.IGNORECASE)
    for message in messages:
        escaped_text = str(escape(message['message']))
        text = replace_str.sub(r"<b>\1</b>", escaped_text)
        messages_for_render.append({
            'number': current_number,
            'text': text,
            'created_at': message['created_at']
        })
        current_number -= 1
    return render_template_string('''
    {% extends 'base.html' %}
    {% block header %}
        <h1>{% block title %}Guestbook{% endblock %}</h1>
    {% endblock %}
    {% block content %}
    {% for message in messages_for_render %}
    <div>
        <h1> Message #{{ message.number }}</h1>
        <p>{{ message.text | safe }}</p>
        <small>Created at {{ message.created_at }}</small>
    </div>
    {% endfor %}
    <a href={{ url_for('guestbook.add_message') }}>Add message</a>
    {% endblock %}
    ''', messages_for_render=messages_for_render)


@bp.route("/add", methods=['GET', 'POST'])
def add_message():
    if request.method == 'POST':
        message = request.form['message']
        db = get_db()
        db.execute("INSERT INTO messages (message, created_at) VALUES (?, datetime('now'))",(message,))
        db.commit()
        return redirect(url_for("guestbook.index"))
    return render_template('guestbook/add.html')