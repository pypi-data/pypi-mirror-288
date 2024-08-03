import unittest

from tests.mocks.common.environment_builder import EnvironmentBuilder

from chilo_api.core.endpoint import Endpoint
from chilo_api.core.resolver.scanner import ResolverScanner


class ResolverScannerTest(unittest.TestCase):
    handlers = 'tests/mocks/handlers/unit_tests/valid'
    base_path = 'unit-test/v1'
    handler_pattern = 'tests/mocks/handlers/unit_tests/valid/**/*_handler.py'

    def test_load_importer_files_pass(self):
        scanner = ResolverScanner(handlers=self.handlers, base_path=self.base_path)
        scanner.load_importer_files()
        self.assertTrue(True)

    def test_get_endpoint_module_pass(self):
        scanner = ResolverScanner(handlers=self.handlers, base_path=self.base_path)
        request = EnvironmentBuilder().get_request(path='/unit-test/v1/basic')
        endpoint_module = scanner.get_endpoint_module(request)
        self.assertTrue(endpoint_module is not None)

    def test_get_endpoint_from_pattern_module_pass(self):
        scanner = ResolverScanner(handlers=self.handler_pattern, base_path=self.base_path)
        request = EnvironmentBuilder().get_request(path='/unit-test/v1/pattern-dynamic')
        endpoint_module = scanner.get_endpoint_module(request)
        self.assertTrue(endpoint_module is not None)

    def test_get_dynamic_endpoint_from_pattern_module_pass(self):
        scanner = ResolverScanner(handlers=self.handler_pattern, base_path=self.base_path)
        request = EnvironmentBuilder().get_request(path='/unit-test/v1/pattern-dynamic/{id}')
        endpoint_module = scanner.get_endpoint_module(request)
        self.assertTrue(endpoint_module is not None)

    def test_get_endpoint_module_fails(self):
        scanner = ResolverScanner(handlers=self.handlers, base_path=self.base_path)
        request = EnvironmentBuilder().get_request(path='/unit-test/v1/basic-miss')
        try:
            scanner.get_endpoint_module(request)
            self.assertTrue(False)
        except Exception as error:
            self.assertTrue('route not found' in str(error))

    def test_reset(self):
        scanner = ResolverScanner(handlers=self.handlers, base_path=self.base_path)
        scanner.has_dynamic_route = True
        scanner.file_tree_climbed = False
        scanner.dynamic_parts = {'key': 'value'}
        scanner.import_path = ['test']
        scanner.reset()
        self.assertEqual(False, scanner.has_dynamic_route)
        self.assertEqual(True, scanner.file_tree_climbed)
        self.assertDictEqual({}, scanner.dynamic_parts)
        self.assertEqual(0, len(scanner.import_path))
