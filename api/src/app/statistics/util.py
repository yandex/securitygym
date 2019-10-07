from collections import OrderedDict

from app.db import get_db


def get_users_all_statistics():
    statistics_table = OrderedDict()
    cursor = get_db().cursor()
    cursor.execute(" SELECT users.uid, users.username, COUNT(users.uid) as total_lessons_count " +
                   " FROM completed_lessons " +
                   " RIGHT JOIN users ON users.uid = completed_lessons.uid " +
                   " GROUP BY users.uid " +
                   " ORDER BY total_lessons_count DESC")
    for statistics_row in cursor.fetchall():
        uid = statistics_row[0]
        username = statistics_row[1]
        total_lessons_count = statistics_row[2]
        statistics_table[uid] = {'uid': uid,
                                               'username': username,
                                               'total_lessons_count': total_lessons_count,
                                               'courses': {} }
    cursor.execute(" SELECT users.uid, completed_lessons.course, COUNT(completed_lessons.lesson) as course_progress_number " +
                   " FROM completed_lessons " +
                   " JOIN users ON users.uid = completed_lessons.uid " +
                   " GROUP BY users.uid, completed_lessons.course " +
                   " ORDER BY users.uid DESC")
    for statistics_row in cursor.fetchall():
        uid = statistics_row[0]
        course_name = statistics_row[1]
        course_progress_number = statistics_row[2]
        if uid in statistics_table:
            statistics_table[uid]['courses'][course_name] = course_progress_number
    return statistics_table
