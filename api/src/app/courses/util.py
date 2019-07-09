import os
import yaml
import re

from flask import url_for

from app.settings import COURSES_PATH


def is_name_valid_for_directory(name):
    return re.match("^[A-Za-z0-9_-]*$", name)


def courses_from_path():
    courses = []
    for name in os.listdir(COURSES_PATH):
        # list all subdirectories from courses
        if os.path.isdir(os.path.join(COURSES_PATH, name)) and is_name_valid_for_directory(name):
            course = {"slug": name, "url": url_for("courses.course_content", course_slug=name)}
            course_path = os.path.join(COURSES_PATH, name)
            if os.path.isfile(os.path.join(course_path, 'index.yaml')):
                # load course description from index.yaml
                yaml_content = open(os.path.join(course_path, 'index.yaml')).read().encode('utf-8')
                course_description = yaml.safe_load(yaml_content)
                course.update(course_description)
            courses.append(course)
    return courses


def course_content_from_path(course_name):
    lessons = []
    course_path = os.path.join(COURSES_PATH, course_name)
    if os.path.isdir(course_path):
        for name in os.listdir(course_path):
            if os.path.isdir(os.path.join(course_path, name)) and is_name_valid_for_directory(name):
                lesson = {"slug": name}
                lesson_path = os.path.join(course_path, name)
                if os.path.isfile(os.path.join(course_path, 'index.yaml')):
                    yaml_content = open(os.path.join(lesson_path, 'index.yaml')).read().encode('utf-8')
                    lesson_description = yaml.safe_load(yaml_content)
                    lesson.update(lesson_description)
                lessons.append(lesson)
    return lessons
