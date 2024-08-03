import os
import importlib.util

from chilo_api import Chilo


class ServerImporter:

    def __init__(self, api):
        cwd = os.getcwd()
        api_file = api if '.py' in api else f'{api}.py'
        self.__file_path = f'{cwd}/{api_file}'
        self.__import_path = self.__file_path.replace('/', '.')

    def get_api_module(self):
        spec = importlib.util.spec_from_file_location(self.__import_path, self.__file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        matches = [v for v in module.__dict__.values() if isinstance(v, Chilo)]
        return matches[0]
