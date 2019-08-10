import os
import yaml
import re
import requests

from flask import url_for
from flask import g

from app.db import get_db
from app.settings import COURSES_PATH
from app.settings import CHECK_EXECUTOR_URL


def is_name_valid_for_directory(name):
    return re.match("^[A-Za-z0-9_-]*$", name)


def get_info_from_index_yaml(dir_path):
    yaml_path = os.path.join(dir_path, 'index.yaml')
    if os.path.isfile(yaml_path):
        yaml_content = open(yaml_path).read().encode('utf-8')
        description = yaml.safe_load(yaml_content)
        return description
    else:
        return dict()


def courses_from_path():
    # get count of solved lessons for every course
    course_lessons_completed = {}
    if g.user is not None:
        cursor = get_db().cursor()
        cursor.execute("SELECT course, COUNT(lesson) FROM completed_lessons WHERE uid=%s GROUP BY course",
                       (g.user['uid'],))
        for course in cursor.fetchall():
            course_lessons_completed[course[0]] = course[1]
    courses = []
    for name in os.listdir(COURSES_PATH):
        # list all subdirectories from courses
        if os.path.isdir(os.path.join(COURSES_PATH, name)) and is_name_valid_for_directory(name):
            course = {"slug": name, "url": url_for("courses.course_content", course_slug=name)}
            course_path = os.path.join(COURSES_PATH, name)
            course_description = get_info_from_index_yaml(course_path)
            course.update(course_description)
            course['solved'] = False
            if name in course_lessons_completed:
                total_lessons = len([i for i in os.listdir(course_path)
                                     if os.path.isdir(os.path.join(course_path, i)) and is_name_valid_for_directory(i)])
                if total_lessons == course_lessons_completed[name]:
                    course['solved'] = True
            courses.append(course)
    return courses


def course_info_from_path(course_name):
    if not is_name_valid_for_directory(course_name):
        return dict()
    course = {"slug": course_name, "url": url_for("courses.course_content", course_slug=course_name)}
    course_path = os.path.join(COURSES_PATH, course_name)
    course_description = get_info_from_index_yaml(course_path)
    course.update(course_description)
    return course


def course_content_from_path(course_name):
    if not is_name_valid_for_directory(course_name):
        return []
    # get all solved lessons for user
    solved_lessons = {}
    if g.user is not None:
        cursor = get_db().cursor()
        cursor.execute("SELECT lesson FROM completed_lessons WHERE uid=%s AND course=%s", (g.user['uid'], course_name))
        for lesson in cursor.fetchall():
            solved_lessons[lesson[0]] = True
    lessons = []
    course_path = os.path.join(COURSES_PATH, course_name)
    if os.path.isdir(course_path):
        for name in os.listdir(course_path):
            if os.path.isdir(os.path.join(course_path, name)) and is_name_valid_for_directory(name):
                lesson = {"slug": name, "url": url_for("courses.lesson_content",
                                                       course_slug=course_name, lesson_slug=name)}
                lesson_path = os.path.join(course_path, name)
                lesson_description = get_info_from_index_yaml(lesson_path)
                lesson.update(lesson_description)
                lesson['solved'] = name in solved_lessons
                lessons.append(lesson)
    return lessons


def lesson_content_from_path(course_name, lesson_name):
    if not is_name_valid_for_directory(course_name) or not is_name_valid_for_directory(lesson_name):
        return {}
    course_path = os.path.join(COURSES_PATH, course_name)
    lesson_path = os.path.join(COURSES_PATH, course_name, lesson_name)
    lesson = {"slug": lesson_name, "course_slug": course_name,
              "url": url_for("courses.lesson_content", course_slug=course_name, lesson_slug=lesson_name)}
    if os.path.isdir(lesson_path):
        course_dict = get_info_from_index_yaml(course_path)
        lesson['course_title'] = course_dict.get('title', course_name)
        lesson_dict = get_info_from_index_yaml(lesson_path)
        if os.path.isdir(os.path.join(lesson_path, 'description')):
            # Get Description from MarkDown file
            # TODO: multilanguage
            if os.path.isfile(os.path.join(lesson_path, 'description', 'ru.md')):
                description_filename = os.path.join(lesson_path, 'description', 'ru.md')
                lesson['description'] = open(description_filename).read()
        # Search for prev/next lesson
        lessons = list(filter(lambda name: os.path.isdir(os.path.join(COURSES_PATH, course_name, name))
                              and is_name_valid_for_directory(name),
                              os.listdir(os.path.join(COURSES_PATH, course_name))))
        curr_index = lessons.index(lesson_name)
        lesson['prev_slug'] = lessons[curr_index - 1] if curr_index > 0 else ''
        lesson['next_slug'] = lessons[curr_index + 1] if curr_index < len(lessons) - 1 else ''
        # Get vulnerable_code
        if 'vulnerable_code_file' in lesson_dict \
                and os.path.isfile(os.path.join(lesson_path, lesson_dict.get('vulnerable_code_file'))):
            lesson['vulnerable_code'] = open(os.path.join(lesson_path, lesson_dict.get('vulnerable_code_file'))).read()
        else:
            lesson['vulnerable_code'] = ''

        lesson['language'] = lesson_dict.get('language', '')
        lesson['title'] = lesson_dict.get('title', lesson_name)
        lesson['solved'] = False
        if g.user is not None:
            cursor = get_db().cursor()
            cursor.execute("SELECT uid, course, lesson FROM completed_lessons "
                           "WHERE uid=%s AND course=%s AND lesson=%s", (g.user['uid'], course_name, lesson_name))
            if cursor.fetchone():
                lesson['solved'] = True
    return lesson


def lesson_check_execute(course_name, lesson_name, code):
    if not is_name_valid_for_directory(course_name) or not is_name_valid_for_directory(lesson_name):
        return {}
    lesson_info = get_info_from_index_yaml(os.path.join(COURSES_PATH, course_name, lesson_name))
    # normalize exclude files
    excluded_files = [os.path.join(COURSES_PATH, course_name, lesson_name, lesson_info.get('vulnerable_code_file', ''))]
    for exclude_file in lesson_info.get('excluded_files', []):
        excluded_files.append(os.path.join(COURSES_PATH, course_name, lesson_name, exclude_file))
    # get all files for
    files = []
    for r, d, f in os.walk(os.path.join(COURSES_PATH, course_name, lesson_name)):
        for file in f:
            file_path = os.path.join(r, file)
            is_excluded = False
            if file_path in excluded_files:
                is_excluded = True
            for exclude_path in excluded_files:
                if exclude_path in file_path:
                    is_excluded = True
                    break
            if not is_excluded:
                files.append({'name': file_path, 'content': open(file_path).read()})
    files.append({
        'name': os.path.join(COURSES_PATH, course_name, lesson_name, lesson_info.get('vulnerable_code_file', '')),
        'content': code
    })
    # profile
    profile = lesson_info.get('profile', '')
    # run command
    run_checks = lesson_info.get('run_checks', '')
    # request to check_executor
    r = requests.post(CHECK_EXECUTOR_URL, json={
        'files': files,
        'profile': profile,
        'command': run_checks
    })
    result = r.json()
    if result['success']:
        if g.user['uid']:
            cursor = get_db().cursor()
            cursor.execute("INSERT INTO completed_lessons (uid, course, lesson) "
                           "VALUES (%s, %s, %s)", (g.user['uid'], course_name, lesson_name))
    return result
