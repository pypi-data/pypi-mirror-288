import unittest

from chilo_api.cli.server.validator import ServerValidator


class MockServer:
    port = 9999999999


class ServerValidatorTest(unittest.TestCase):

    def test_validate(self):
        server = MockServer()
        validator = ServerValidator()
        try:
            validator.validate(server)
            self.assertTrue(False)
        except RuntimeError as error:
            self.assertTrue('is not between well knonwn ports' in str(error))
