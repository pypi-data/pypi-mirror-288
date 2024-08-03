from unittest import mock, TestCase

from chilo_api.cli.server import run_server


class MockArgs:
    api = 'api.py'
    host = '127.0.0.1'
    port = 3000
    reload = False
    verbose = False


def mock_run_simple(*args, **kwargs):
    pass


class RunServerTest(TestCase):

    @mock.patch('chilo_api.cli.server.run_simple', mock_run_simple)
    def test_run_server(self):
        args = MockArgs()
        run_server(args)  # should throw an error if every broken
        self.assertTrue(True)
