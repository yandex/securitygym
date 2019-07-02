import os
import tempfile
from sqli.vuln_app import create_app
from sqli.tests.test_functional import TestArticlesSearchFunctional
from sqli.tests.test_security import TestSQLSecurity


def run_tests(test_class, app, client):
    result = True
    test_obj = test_class()
    for method_name in dir(test_class):
        if not method_name.startswith('_') and not method_name.startswith('test'):
            method = getattr(test_obj, method_name)
            (test_result, message) = method(app, client)
            print(message)
            if not test_result:
                result = False
    return result


if __name__ == '__main__':
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"DATABASE": db_path})
    client = app.test_client()
    success = True
    if run_tests(TestArticlesSearchFunctional, app, client):
        print("Functional tests passed")
    else:
        success = False
        print("Functional tests failed")
    if run_tests(TestSQLSecurity, app, client):
        print("Security tests passed")
    else:
        success = False
        print("Security tests failed")
    os.close(db_fd)
    os.unlink(db_path)
    if success:
        exit(0)
    else:
        exit(1)
