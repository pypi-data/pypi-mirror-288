import unittest

from chilo_api.cli.server.arguments import ServerArguments


class MockArgs:
    api = 'api.py'
    host = '127.0.0.1'
    port = 3000
    reload = False
    verbose = False


class MockApi:
    api = 'api.py'
    host = '127.0.0.1'
    port = 3000
    reload = False
    verbose = False
    timeout = None
    openapi_validate_request = False
    openapi_validate_response = False

    def route(self, *args, **kwargs):
        pass


class ArgumentsTest(unittest.TestCase):

    def test_route(self):
        mock_args = MockArgs()
        mock_api = MockApi()
        server_args = ServerArguments(mock_args, mock_api)
        server_args.route(environ={}, server_response={})
