from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash

import yaml

bp = Blueprint("config", __name__)


@bp.route("/", methods=("GET", "POST"))
def config():
    if request.method == "POST":
        file = request.files['file']
        if file:
            yaml_content = file.read().decode('utf-8')
            try:
                config_map = yaml.unsafe_load(yaml_content)
                if not isinstance(config_map, dict):
                    config_map = {'config': config_map}
                flash("YAML file successfully loaded")
                return render_template("config/form.html", config_map=config_map)
            except yaml.YAMLError:
                flash("Incorrect YAML file")
                return render_template("config/form.html")
    return render_template("config/form.html")