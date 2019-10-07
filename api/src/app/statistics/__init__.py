from flask import Blueprint
from flask import jsonify

from app.statistics.util import get_users_all_statistics
from app.courses.util import courses_from_path

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
