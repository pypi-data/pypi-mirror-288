from art import tprint


class ServerLogger:  # pragma: no cover

    def log_start(self):
        print('=========== STARTING ===========')

    def log_logo(self):
        tprint('CHILO')

    def log_settings(self, server):
        print('|--------------------- settings ---------------------|')
        print(f'| HOST: {server.host} (from {server.source["host"]})')
        print(f'| PORT: {server.port} (from {server.source["port"]})')
        print(f'| RELOAD: {server.reload} (from {server.source["reload"]})')
        print(f'| VERBOSE: {server.verbose} (from {server.source["verbose"]})')
        print(f'| TIMEOUT: {server.timeout}')
        print(f'| OPENAPI REQUEST VALIDATION: {server.openapi_validate_request}')
        print(f'| OPENAPI RESPONSE VALIDATION: {server.openapi_validate_response}')
        print('|----------------------------------------------------|')
        print('\n')
