import argparse

from chilo_api.cli.openapi import generate_openapi
from chilo_api.cli.server import run_server


class CliManager:

    def __init__(self):
        self.__args = self.__get_command_line_args()

    @property
    def args(self):
        return self.__args

    def run(self):
        if self.args.action == 'generate-openapi':
            generate_openapi(self.args)
        elif self.args.action == 'serve':
            run_server(self.args)

    def __get_command_line_args(self):
        parser = argparse.ArgumentParser(
            prog='Chilo',
            description='Chilo CLI Tool'
        )
        parser.add_argument(
            'action',
            help='the action to take',
            choices=['generate-openapi', 'serve']
        )
        parser.add_argument(
            '-a',
            '--api',
            help='api file to run',
            required=False
        )
        parser.add_argument(
            '-o',
            '--output',
            help='(optional) directory location to save openapi file; defaults handlers directory location',
            required=False
        )
        parser.add_argument(
            '-f',
            '--format',
            help='(optional) comma deliminted format options (yml, json)',
            choices=['yml', 'json', 'yml,json', 'json,yml'],
            required=False
        )
        parser.add_argument(
            '-d',
            '--delete',
            help='(optional) will delete routes and methods not found in code base',
            action='store_true',
            required=False
        )
        parser.add_argument(
            '-s',
            '--host',
            help='(optional) host ip/domain for server; default: 127.0.0.1',
            default='127.0.0.1',
            required=False
        )
        parser.add_argument(
            '-p',
            '--port',
            help='(optional) port to run server on; default 3000',
            default=3000,
            required=False
        )
        parser.add_argument(
            '-r',
            '--reload',
            help='(optional) will reload app on file change; default: False',
            required=False
        )
        parser.add_argument(
            '-v',
            '--verbose',
            help='(optional) will run server in verbose/debug mode; default: False',
            required=False
        )
        return parser.parse_args()
