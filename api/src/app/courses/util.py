import os
import yaml
import re

from flask import url_for

from app.settings import COURSES_PATH


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
    courses = []
    for name in os.listdir(COURSES_PATH):
        # list all subdirectories from courses
        if os.path.isdir(os.path.join(COURSES_PATH, name)) and is_name_valid_for_directory(name):
            course = {"slug": name, "url": url_for("courses.course_content", course_slug=name)}
            course_path = os.path.join(COURSES_PATH, name)
            course_description = get_info_from_index_yaml(course_path)
            course.update(course_description)
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
    lessons = []
    course_path = os.path.join(COURSES_PATH, course_name)
    if os.path.isdir(course_path):
        for name in os.listdir(course_path):
            if os.path.isdir(os.path.join(course_path, name)) and is_name_valid_for_directory(name):
                lesson = {"slug": name}
                lesson_path = os.path.join(course_path, name)
                lesson_description = get_info_from_index_yaml(lesson_path)
                lesson.update(lesson_description)
                lessons.append(lesson)
    return lessons
