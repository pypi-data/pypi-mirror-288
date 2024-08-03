import json
import unittest

from tests.mocks.common.environment_builder import EnvironmentBuilder

from chilo_api.core.endpoint import Endpoint
from chilo_api.core.resolver.importer import ResolverImporter


class EndpointTest(unittest.TestCase):
    handler_path = 'tests/mocks/handlers/unit_tests/valid'
    file_path = f'{handler_path}/basic.py'
    import_path = 'tests.mocks.handlers.basic'
    environ = EnvironmentBuilder()

    def __get_endpoint_instance(self, method):
        importer = ResolverImporter(handlers=self.handler_path)
        endpoint_module = importer.import_module_from_file(self.file_path, self.import_path)
        return Endpoint(endpoint_module, method)

    def test_module(self):
        endpoint = self.__get_endpoint_instance('post')
        self.assertTrue('tests.mocks.handlers.basic', endpoint.module.__name__)

    def test_endpoint_initializes(self):
        endpoint = self.__get_endpoint_instance('post')
        self.assertTrue(isinstance(endpoint, Endpoint))

    def test_endpoint_has_requirements(self):
        endpoint = self.__get_endpoint_instance('post')
        self.assertTrue(endpoint.has_requirements)

    def test_endpoint_has_no_requirements(self):
        endpoint = self.__get_endpoint_instance('patch')
        self.assertFalse(endpoint.has_requirements)

    def test_endpoint_requires_auth(self):
        endpoint = self.__get_endpoint_instance('post')
        self.assertTrue(endpoint.requires_auth)

    def test_endpoint_has_required_response(self):
        endpoint = self.__get_endpoint_instance('search')
        self.assertTrue(endpoint.has_required_response)

    def test_endpoint_has_required_route(self):
        endpoint = self.__get_endpoint_instance('delete')
        self.assertTrue(endpoint.has_required_route)
        self.assertEqual('/some/route/{id}', endpoint.required_route)

    def test_endpoint_supports_custom_requirements(self):
        endpoint = self.__get_endpoint_instance('put')
        self.assertTrue(endpoint.has_requirements)
        self.assertDictEqual({'custom_list': [1, 2, 3], 'custom_dict': {'key': 'value'}, 'custom_simple': 1}, endpoint.requirements)

    def test_endpoint_runs_with_requirements(self):
        endpoint = self.__get_endpoint_instance('post')
        response = self.environ.get_response()
        request = self.environ.get_request()
        result = endpoint.run(request, response)
        body = next(result.server).decode('utf-8')
        self.assertDictEqual({'router_directory_basic': ''}, json.loads(body))

    def test_endpoint_runs_without_requirements(self):
        endpoint = self.__get_endpoint_instance('patch')
        response = self.environ.get_response()
        request = self.environ.get_request()
        result = endpoint.run(request, response)
        body = next(result.server).decode('utf-8')
        self.assertEqual({'router_directory_basic': 'PATCH'}, json.loads(body))

    def test_run_options(self):
        endpoint = self.__get_endpoint_instance('options')
        response = self.environ.get_response()
        request = self.environ.get_request()
        result = endpoint.run(request, response)
        control_methods = result.headers['Access-Control-Request-Method']
        self.assertEqual('DELETE,GET,PATCH,POST,PUT', control_methods)

    def test_run_head(self):
        endpoint = self.__get_endpoint_instance('head')
        response = self.environ.get_response()
        request = self.environ.get_request()
        result = endpoint.run(request, response)
        x_header = result.headers['x-new-header']
        self.assertEqual('NEW-HEADER', x_header)
