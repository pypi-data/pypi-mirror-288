import unittest
from unittest.mock import patch

from chilo_api.cli import CliManager


def mock_run(*args, **kwargs):
    pass


class CliManagerTest(unittest.TestCase):

    @patch('chilo_api.cli.generate_openapi', mock_run)
    @patch('sys.argv', [
        'CliManager',
        'generate-openapi',
        '--api=api',
        '--output=tests',
        '--format=json,yml',
        '--delete'
    ])
    def test_args(self):
        manager = CliManager()
        manager.run()
        self.assertEqual('api', manager.args.api)
        self.assertEqual('tests', manager.args.output)
        self.assertListEqual(['json', 'yml'], manager.args.format.split(','))
        self.assertTrue(manager.args.delete)

    @patch('chilo_api.cli.run_server', mock_run)
    @patch('sys.argv', [
        'CliManager',
        'serve',
        '--api=api'
    ])
    def test_run(self):
        manager = CliManager()
        manager.run()
        self.assertEqual('api', manager.args.api)
