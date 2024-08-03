from chilo_api.core.validator.openapi import OpenApiValidator
import unittest
import warnings

warnings.filterwarnings('ignore')


class OpenApiValidatorTest(unittest.TestCase):
    valid_schema = 'tests/mocks/openapi/variations/openapi.yml'
    invalid_schema = 'tests/mocks/openapi/variations/openapi-for-validator-test-fail.yml'
    missing_required_body = 'tests/mocks/openapi/variations/openapi-missing-required-body.yml'
    missing_required_response = 'tests/mocks/openapi/variations/openapi-missing-required-response.yml'
    openapi_validate_request_schema_pass = 'tests/mocks/openapi/variations/openapi-auto-validate-pass.yml'
    openapi_validate_request_schema_route_fail_route = 'tests/mocks/openapi/variations/openapi-auto-validate-route-fail-route.yml'
    openapi_validate_request_schema_route_fail_method = 'tests/mocks/openapi/variations/openapi-auto-validate-route-fail-route-method.yml'

    def test_valid_openapi(self):
        validator = OpenApiValidator(openapi=self.valid_schema, handlers='tests/mocks/handlers/unit_tests/valid')
        validator.validate_openapi()

    def test_invalide_openapi_spec_errors(self):
        validator = OpenApiValidator(openapi=self.invalid_schema, handlers='tests/mocks/handlers/unit_tests/valid')
        try:
            validator.validate_openapi()
            self.assertTrue(False)
        except RuntimeError as error:
            self.assertIn('there was a problem with your openapi schema; see above', str(error))

    def test_invalid_openapi_spec_ignored(self):
        validator = OpenApiValidator(openapi=self.invalid_schema, openapi_validate_spec=False, handlers='tests/mocks/handlers/unit_tests/valid')
        validator.validate_openapi()
        self.assertTrue(True)

    def test_handler_spec_passes_openapi(self):
        validator = OpenApiValidator(openapi=self.openapi_validate_request_schema_pass,
                                     handlers='tests/mocks/handlers/unit_tests/valid', openapi_validate_request=True)
        validator.validate_openapi()

    def test_handler_spec_route_not_in_openapi(self):
        validator = OpenApiValidator(openapi=self.openapi_validate_request_schema_route_fail_route,
                                     handlers='tests/mocks/handlers/unit_tests/valid', openapi_validate_request=True)
        try:
            validator.validate_openapi()
            self.assertTrue(False)
        except RuntimeError as error:
            print(error)
            self.assertIn('openapi_validate_request is enabled and route', str(error))

    def test_handler_spec_route_method_not_in_openapi(self):
        validator = OpenApiValidator(openapi=self.openapi_validate_request_schema_route_fail_method,
                                     handlers='tests/mocks/handlers/unit_tests/valid', openapi_validate_request=True)
        try:
            validator.validate_openapi()
            self.assertTrue(False)
        except RuntimeError as error:
            print(error)
            self.assertIn('openapi_validate_request is enabled and method', str(error))

    def test_handler_spec_fails_missing_schema_defined_in_required_body(self):
        validator = OpenApiValidator(openapi=self.missing_required_body, handlers='tests/mocks/handlers/unit_tests/valid')
        try:
            validator.validate_openapi()
            self.assertTrue(False)
        except RuntimeError as error:
            self.assertIn('required_body schema', str(error))

    def test_handler_spec_fails_missing_schema_defined_in_required_response(self):
        validator = OpenApiValidator(openapi=self.missing_required_response, handlers='tests/mocks/handlers/unit_tests/valid')
        try:
            validator.validate_openapi()
            self.assertTrue(False)
        except RuntimeError as error:
            self.assertIn('required_response schema', str(error))
