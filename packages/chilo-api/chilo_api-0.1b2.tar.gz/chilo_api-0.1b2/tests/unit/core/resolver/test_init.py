import unittest

from tests.mocks.common.environment_builder import EnvironmentBuilder

from chilo_api.core.exception import ApiException
from chilo_api.core.endpoint import Endpoint
from chilo_api.core.resolver import Resolver


class ResolverTest(unittest.TestCase):
    base_path = 'unit-test/v1'
    handler_path = 'tests/mocks/handlers/unit_tests/valid'
    bad_handler_path = 'tests/mocks/handlers/unit_tests/invalid/bad_endpoint'
    environ = EnvironmentBuilder()

    def test_finding_endpoint_passes(self):
        request = self.environ.get_request(path='unit-test/v1/basic')
        resolver = Resolver(base_path=self.base_path, handlers=self.handler_path)
        endpoint = resolver.get_endpoint(request)
        self.assertTrue(isinstance(endpoint, Endpoint))

    def test_finding_endpoint_fails_no_route(self):
        request = self.environ.get_request(path='unit-test/v1/bad')
        resolver = Resolver(base_path=self.base_path, handlers=self.handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('route not found', api_error.message)

    def test_finding_endpoint_fails_dynamic_endpoint_bad_route_definition(self):
        request = self.environ.get_request(path='unit-test/v1/bad_dynamic/1', method='post')
        resolver = Resolver(base_path=self.base_path, handlers=self.handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('no route found; requested dynamic route does not match endpoint route definition', api_error.message)

    def test_finding_endpoint_fails_dynamic_endpoint_bad_route_variable(self):
        request = self.environ.get_request(path='unit-test/v1/bad_dynamic/1', method='get')
        resolver = Resolver(base_path=self.base_path, handlers=self.bad_handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('no route found; endpoint does not have proper variables in required_route', api_error.message)

    def test_finding_endpoint_fails_dynamic_endpoint_no_required_route_param(self):
        request = self.environ.get_request(path='unit-test/v1/bad_dynamic/1', method='patch')
        resolver = Resolver(base_path=self.base_path, handlers=self.bad_handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('no route found; endpoint does have required_route configured', api_error.message)

    def test_finding_endpoint_fails_dynamic_endpoint_bad_route_definition(self):
        request = self.environ.get_request(path='unit-test/v1/bad_dynamic/1', method='post')
        resolver = Resolver(base_path=self.base_path, handlers=self.bad_handler_path)
        try:
            resolver.get_endpoint(request)
            self.assertTrue(False)
        except ApiException as api_error:
            self.assertEqual('no route found; requested dynamic route does not match endpoint route definition', api_error.message)

    def test_finding_dynamic_endpoint_passes(self):
        request = self.environ.get_request(path='unit-test/v1/bad-dynamic/1', method='delete')
        resolver = Resolver(base_path=self.base_path, handlers=self.bad_handler_path)
        endpoint = resolver.get_endpoint(request)
        self.assertTrue(isinstance(endpoint, Endpoint))

    def test_finding_endpoint_from_cache_works(self):
        request = self.environ.get_request(path='unit-test/v1/basic')
        resolver = Resolver(base_path=self.base_path, handlers=self.handler_path)
        self.assertEqual(0, resolver.cache_misses)
        resolver.get_endpoint(request)
        self.assertEqual(1, resolver.cache_misses)
        resolver.get_endpoint(request)
        self.assertEqual(1, resolver.cache_misses)
