import unittest

from chilo_api.core.resolver.importer import ResolverImporter


class ResolverImporterTest(unittest.TestCase):

    def test_bad_handlers_multi_dynamic_files(self):
        importer = ResolverImporter(handlers='tests/mocks/handlers/unit_tests/invalid/bad_structure/multi_dynamic')
        try:
            importer.get_handlers_file_tree()
            self.assertTrue(False)
        except RuntimeError as error:
            self.assertTrue('Cannot have two dynamic files in the same directory' in str(error))
        except:
            self.assertTrue(False)

    def test_bad_handlers_same_file_and_directory_names(self):
        importer = ResolverImporter(handlers='tests/mocks/handlers/unit_tests/invalid/bad_structure/same_names')
        try:
            importer.get_handlers_file_tree()
            self.assertTrue(False)
        except RuntimeError as error:
            self.assertTrue('Cannot have file and directory share same name' in str(error))
        except Exception as error:
            self.assertTrue(False)

    def test_empty_handlers_result(self):
        importer = ResolverImporter(handlers='tests/mocks/empty_handlers')
        try:
            importer.get_handlers_file_tree()
            self.assertTrue(False)
        except RuntimeError as error:
            self.assertTrue('no files found in handler path' in str(error))
        except Exception as error:
            self.assertTrue(False)
