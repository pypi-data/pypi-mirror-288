class ServerValidator:

    def validate(self, server):
        if not 0 <= server.port <= 9999:
            raise RuntimeError(f'port {server.port} is not between well knonwn ports 0 - 9999')
