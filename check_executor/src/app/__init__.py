from flask import Flask
from flask import request
from flask import jsonify
from celery import Celery

from app.util import check


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.update(
        CELERY_BROKER_URL='redis://redis:6379',
        CELERY_RESULT_BACKEND='redis://redis:6379',
        CELERY_TASK_TRACK_STARTED = True,
        CELERY_SEND_EVENTS = True
    )

    celery = Celery(app.import_name, 
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    @celery.task(bind=True)
    def check_solution(self, course, lesson, submitted_files, profile, command):
        self.update_state(state='PROGRESS')
        files = []
        for file in submitted_files:
            files.append({
                'name': file.get('name', ''),
                'content': file.get('content', '').encode('utf-8')
            })
        check_result = check(profile, command, files)
        is_success = check_result['exit_code'] == 0
        debug_console = check_result['stdout'] if check_result['stdout'] else check_result['stderr']
        if check_result['oom_killed']: debug_console += "\nError: Out Of Memory".encode('utf-8')
        if check_result['timeout']: debug_console += "\nError: Timeout".encode('utf-8')
        message = 'Congratulation! You have solved this task!' if is_success else 'Some tests failed. Try harder:)'
        return {
            'course': course,
            'lesson': lesson,
            'success': is_success,
            'message': message,
            'console': debug_console.decode('utf-8')
        }

    @app.route("/run_check", methods=['POST'])
    def run_check():
        r = request.json
        task = check_solution.apply_async(args=[r.get('course', ''), r.get('lesson', ''), r.get('files', []), r.get('profile', ''), r.get('command', '')])
        return jsonify({
            'task_id': task.id,
            'state': task.state
        })

    @app.route("/check_results/<string:task_id>", methods=['GET'])
    def check_results(task_id):
        task = check_solution.AsyncResult(task_id)
        if task.state == 'PENDING' or task.state == 'PROGRESS':
            response = {
                'state': task.state
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'success': task.info.get('success', False),
                'message': task.info.get('message', ''),
                'console': task.info.get('console', ''),
                'course': task.info.get('course', ''),
                'lesson': task.info.get('lesson', ''),
            }
        else:
            response = {
                'state': task.state,
                'success': False,
                'message': 'Internal Error',
                'console': str(task.info)
            }
        return jsonify(response)

    return (app, celery)
