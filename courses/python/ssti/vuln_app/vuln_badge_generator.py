from flask import Blueprint
from flask import request
from flask import render_template
from flask import render_template_string

from time import gmtime, strftime

bp = Blueprint("badge_generator", __name__)


@bp.route("/", methods=("GET", "POST"))
def generate():
    if request.method == "POST":
        username = request.form['username']
        badge = ('<p><h3>%s</h3><ul><li><b>Rank:</b> Hacker</li><li><b>Total points:</b> 1337</li></ul>' + \
                 '<small>Generated at %s</small></p>') % (username, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        return render_template_string('''
        {% extends 'base.html' %}

        {% block header %}
            <h1>{% block title %}Badge{% endblock %}</h1>
        {% endblock %}
        
        {% block content %}
        <hr/>
        ''' + badge + '''
        <hr/>
        {% endblock %}
        ''')
    return render_template("badge/form.html")
