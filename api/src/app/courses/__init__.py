from flask import Blueprint
from flask import jsonify
from flask import abort
from flask import request

from app.auth import login_required
from app.courses.util import is_name_valid_for_directory
from app.courses.util import courses_from_path
from app.courses.util import course_info_from_path
from app.courses.util import course_content_from_path
from app.courses.util import lesson_content_from_path
from app.courses.util import lesson_check_execute

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


@bp.route('/<string:course_slug>/lessons/<string:lesson_slug>', methods=['GET'])
def lesson_content(course_slug, lesson_slug):
    if not is_name_valid_for_directory(course_slug) or not is_name_valid_for_directory(lesson_slug):
        abort(404)
    lesson = lesson_content_from_path(course_slug, lesson_slug)
    return jsonify(lesson)


@bp.route('/<string:course_slug>/lessons/<string:lesson_slug>/check', methods=['POST'])
@login_required
def lesson_check_code(course_slug, lesson_slug):
    if not is_name_valid_for_directory(course_slug) or not is_name_valid_for_directory(lesson_slug):
        abort(404)
    r = request.json
    result = lesson_check_execute(course_slug, lesson_slug, r['code'])
    return jsonify(result)
