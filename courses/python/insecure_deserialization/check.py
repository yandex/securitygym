import os
import tempfile
from insecure_deserialization.vuln_app import create_app
from insecure_deserialization.tests.test_functional import TestYAMLFunctional
from insecure_deserialization.tests.test_security import TestYAMLSecurity


def run_tests(test_class, client):
    result = True
    test_obj = test_class()
    for method_name in dir(test_class):
        if not method_name.startswith('_') and not method_name.startswith('test'):
            method = getattr(test_obj, method_name)
            (test_result, message) = method(client)
            print(message)
            if not test_result:
                result = False
    return result


if __name__ == '__main__':
    app = create_app()
    client = app.test_client()
    success = True
    if run_tests(TestYAMLFunctional, client):
        print("Functional tests passed")
    else:
        success = False
        print("Functional tests failed")
    if run_tests(TestYAMLSecurity, client):
        print("Security tests passed")
    else:
        success = False
        print("Security tests failed")
    if success:
        exit(0)
    else:
        exit(1)
