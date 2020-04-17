from flask import Blueprint
from flask import jsonify
from flask import abort

from app.statistics.util import get_users_all_statistics
from app.statistics.util import get_users_for_course_statistics
from app.courses.util import courses_from_path
from app.courses.util import course_content_from_path
from app.courses.util import is_name_valid_for_directory

bp = Blueprint('statistics', __name__, url_prefix='/statistics')


@bp.route('/', methods=['GET'])
def all_statistics():
    users_table = get_users_all_statistics()
    courses = courses_from_path()
    statistics_table = []
    for row in users_table.values():
        statistics_row = {
            'uid': row['uid'],
            'username': row['username'],
            'courses': {},
        }
        for course in courses:
            if course['slug'] in row['courses']:
                if course['total_lessons'] != 0:
                    progress = 100.0 * row['courses'][course['slug']] / course['total_lessons']
                else:
                    progress = 0
                statistics_row['courses'][course['slug']] = {
                    'progress': progress,
                }
            else:
                statistics_row['courses'][course['slug']] = {
                    'progress': 0,
                }
        statistics_table.append(statistics_row)
    return jsonify({
        'statistics_header': courses,
        'statistics_content': statistics_table,
    })


@bp.route('/courses/<string:course_slug>', methods=['GET'])
def course_statistics(course_slug):
    if not is_name_valid_for_directory(course_slug):
        abort(404)
    users_table = get_users_for_course_statistics(course_slug)
    lessons = course_content_from_path(course_slug)
    statistics_table = []
    for row in users_table.values():
        statistics_row = {
            'uid': row['uid'],
            'username': row['username'],
            'lessons': {},
        }
        for lesson in lessons:
            statistics_row['lessons'][lesson['slug']] = {
                'progress': lesson['slug'] in row['lessons'] and row['lessons'][lesson['slug']] == True,
            }
        statistics_table.append(statistics_row)
    return jsonify({
        'statistics_header': lessons,
        'statistics_content': statistics_table
    })
