import unittest
import json

from tests.mocks.common.environment_builder import EnvironmentBuilder
from tests.mocks.handlers.unit_tests.valid import full_handler as full

from chilo_api.core.exception import ApiTimeOutException


class RequirementsTest(unittest.TestCase):
    environ = EnvironmentBuilder()

    def __get_request_response(self,  timeout=None):
        request = self.environ.get_request(timeout)
        response = self.environ.get_response()
        return request, response

    def test_requirements_decorator_has_attribute(self):
        self.assertTrue(hasattr(full.get, 'requirements'))

    def test_requirements_runs_before(self):
        request, response = self.__get_request_response()
        full.post(request, response)
        self.assertTrue(full.before_call.has_been_called)

    def test_requirements_runs_after(self):
        request, response = self.__get_request_response()
        full.post(request, response)
        self.assertTrue(full.after_call.has_been_called)

    def test_requirements_runs_in_correct_order(self):
        request, response = self.__get_request_response()
        full.post(request, response)
        self.assertEqual('before', full.call_order[0])
        self.assertEqual('after', full.call_order[1])

    def test_requirements_passes_after_request_class(self):
        request, response = self.__get_request_response()
        full.post(request, response)
        body = next(response.server).decode('utf-8')
        self.assertDictEqual({'requirements_basic': True}, json.loads(body))

    def test_requirements_global_timeout_raises_exception(self):
        request, response = self.__get_request_response(timeout=1)
        try:
            full.get(request, response)
            self.assertTrue(False)
        except ApiTimeOutException as error:
            self.assertTrue(isinstance(error, ApiTimeOutException))

    def test_requirements_local_timeout_raises_exception(self):
        request, response = self.__get_request_response()
        try:
            full.patch(request, response)
            self.assertTrue(False)
        except ApiTimeOutException as error:
            self.assertTrue(isinstance(error, ApiTimeOutException))

    def test_requirements_local_overwrites_global_timeout_setting(self):
        request, response = self.__get_request_response(timeout=10)
        try:
            full.patch(request, response)
            self.assertTrue(False)
        except ApiTimeOutException as error:
            self.assertTrue(isinstance(error, ApiTimeOutException))
