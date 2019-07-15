import os
import tempfile
from csrf.vuln_app import create_app
from csrf.tests.conftest import AuthActions
from csrf.tests.test_functional import TestPaymentFunctional
from csrf.tests.test_security import TestCSRFProtection


def run_tests(test_class, app, client, auth):
    result = True
    test_obj = test_class()
    for method_name in dir(test_class):
        if not method_name.startswith('_') and not method_name.startswith('test'):
            method = getattr(test_obj, method_name)
            (test_result, message) = method(app, client, auth)
            print(message)
            if not test_result:
                result = False
    return result


if __name__ == '__main__':
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"DATABASE": db_path})
    client = app.test_client()
    auth = AuthActions(client)
    success = True
    if run_tests(TestPaymentFunctional, app, client, auth):
        print("Functional tests passed")
    else:
        success = False
        print("Functional tests failed")
    if run_tests(TestCSRFProtection, app, client, auth):
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
