from flask import Blueprint
from flask import jsonify
from flask import abort

from app.courses.util import is_name_valid_for_directory
from app.courses.util import courses_from_path
from app.courses.util import course_info_from_path
from app.courses.util import course_content_from_path

bp = Blueprint('courses', __name__, url_prefix='/courses')


@bp.route('/', methods=['GET'])
def courses_list():
    courses = courses_from_path()
    return jsonify(courses)


@bp.route('/<string:course_slug>', methods=['GET'])
def course_info(course_slug):
    if not is_name_valid_for_directory(course_slug):
        abort(404)
    course = course_info_from_path(course_slug)
    return jsonify(course)


@bp.route('/<string:course_slug>/lessons', methods=['GET'])
def course_content(course_slug):
    if not is_name_valid_for_directory(course_slug):
        abort(404)
    lessons = course_content_from_path(course_slug)
    return jsonify(lessons)
