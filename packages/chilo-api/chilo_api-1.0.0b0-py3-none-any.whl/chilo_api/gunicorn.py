from chilo_api.cli.server.importer import ServerImporter  # pragma: no cover


def run(*_, **kwargs):  # pragma: no cover
    importer = ServerImporter(api=kwargs['api'])
    api = importer.get_api_module()
    return api.route
