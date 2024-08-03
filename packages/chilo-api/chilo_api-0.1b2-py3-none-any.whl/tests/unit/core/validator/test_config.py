import unittest

from chilo_api.core.validator.config import ConfigValidator


class ConfigValidatorTest(unittest.TestCase):

    def test_config_validator_validates_all_passing(self):
        try:
            ConfigValidator.validate(
                base_path='some/path',
                handlers='some/path',
                openapi='some/path',
                openapi_validate_request=False,
                openapi_validate_response=False,
                cache_size=128,
                cache_mode='all',
                verbose=True
            )
            self.assertTrue(True)
        except RuntimeError as _:
            self.assertTrue(False)

    def test_config_validator_validates_base_path(self):
        try:
            ConfigValidator.validate(**{})
        except RuntimeError as runtime_error:
            self.assertTrue(isinstance(runtime_error, RuntimeError))
            self.assertEqual('base_path string is required', str(runtime_error))

    def test_config_validator_validates_routing_handlers_is_required(self):
        try:
            ConfigValidator.validate(base_path='some/path')
            self.assertTrue(False)
        except RuntimeError as runtime_error:
            self.assertTrue(isinstance(runtime_error, RuntimeError))
            self.assertEqual('handlers is required; must be glob pattern string {route: file_path}', str(runtime_error))

    def test_config_validator_validates_routing_handlers_are_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers=1)
            self.assertTrue(False)
        except RuntimeError as runtime_error:
            self.assertTrue(isinstance(runtime_error, RuntimeError))
            self.assertEqual('handlers is required; must be glob pattern string {route: file_path}', str(runtime_error))

    def test_config_validator_validates_routing_openapi_validate_request_is_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers='some/path', openapi_validate_request=1)
            self.assertTrue(False)
        except RuntimeError as runtime_error:
            self.assertTrue(isinstance(runtime_error, RuntimeError))
            self.assertEqual('openapi_validate_request should be a boolean', str(runtime_error))

    def test_config_validator_validates_routing_openapi_validate_response_is_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers='some/path', openapi_validate_response=1)
            self.assertTrue(False)
        except RuntimeError as runtime_error:
            self.assertTrue(isinstance(runtime_error, RuntimeError))
            self.assertEqual('openapi_validate_response should be a boolean', str(runtime_error))

    def test_config_validator_validates_routing_verbose_logging_is_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers='some/path', verbose=1)
            self.assertTrue(False)
        except RuntimeError as runtime_error:
            self.assertTrue(isinstance(runtime_error, RuntimeError))
            self.assertEqual('verbose should be a boolean', str(runtime_error))

    def test_config_validator_validates_routing_schema_is_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers='some/path', openapi=1)
            self.assertTrue(False)
        except RuntimeError as runtime_error:
            self.assertTrue(isinstance(runtime_error, RuntimeError))
            self.assertEqual('schema should either be file path string', str(runtime_error))

    def test_config_validator_validates_routing_cache_size_is_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers='some/path', cache_size='1')
            self.assertTrue(False)
        except RuntimeError as runtime_error:
            self.assertTrue(isinstance(runtime_error, RuntimeError))
            self.assertEqual('cache_size should be an int (0 for unlimited size) or None (to disable route caching)', str(runtime_error))

    def test_config_validator_validates_routing_cache_mode_is_appropriate(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers='some/path', cache_mode='bad')
            self.assertTrue(False)
        except RuntimeError as runtime_error:
            self.assertTrue(isinstance(runtime_error, RuntimeError))
            self.assertEqual('cache_mode should be a string of the one of the following values: all, static-only, dynamic-only', str(runtime_error))

    def test_config_schema_is_required_for_openapi_validate_request(self):
        try:
            ConfigValidator.validate(base_path='some/path', handlers='some/path', openapi_validate_request=True)
            self.assertTrue(False)
        except RuntimeError as runtime_error:
            self.assertTrue(isinstance(runtime_error, RuntimeError))
            self.assertEqual('schema is required to use openapi_validate_request', str(runtime_error))
