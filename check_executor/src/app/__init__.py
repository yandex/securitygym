from flask import Flask
from flask import request
from flask import jsonify

from app.util import check


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False

    @app.route("/run_check", methods=['POST'])
    def run_check():
        r = request.json
        files = []
        for file in r.get('files', []):
            files.append({
                'name': file.get('name', ''),
                'content': file.get('content', '').encode('utf-8')
            })
        check_result = check(r.get('profile', ''), r.get('command', ''), files)
        is_success = check_result['exit_code'] == 0
        debug_console = check_result['stdout'] if check_result['stdout'] else check_result['stderr']
        message = 'Congratulation! You have solved this task!' if is_success else 'Some tests failed. Try harder:)'
        return jsonify({
            'success': is_success,
            'message': message,
            'console': debug_console.decode('utf-8')
        })

    return app
