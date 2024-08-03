from werkzeug.serving import run_simple


from chilo_api.cli.server.arguments import ServerArguments
from chilo_api.cli.server.importer import ServerImporter
from chilo_api.cli.server.logger import ServerLogger
from chilo_api.cli.server.validator import ServerValidator


def __start_server(server):
    run_simple(
        server.host,
        server.port,
        server.route,
        use_reloader=server.reload,
        use_debugger=server.verbose
    )


def __get_server(args):
    importer = ServerImporter(args.api)
    api = importer.get_api_module()
    return ServerArguments(args, api)


def run_server(args):
    validaitor = ServerValidator()
    logger = ServerLogger()

    logger.log_start()
    logger.log_logo()

    server = __get_server(args)
    logger.log_settings(server)

    validaitor.validate(server)

    __start_server(server)
