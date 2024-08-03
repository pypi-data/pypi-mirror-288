import unittest

from chilo_api.cli.server.importer import ServerImporter
from chilo_api import Chilo


class ServerImporterTest(unittest.TestCase):

    def test_get_api_module(self):
        importer = ServerImporter('api.py')
        result = importer.get_api_module()
        self.assertTrue(isinstance(result, Chilo))
