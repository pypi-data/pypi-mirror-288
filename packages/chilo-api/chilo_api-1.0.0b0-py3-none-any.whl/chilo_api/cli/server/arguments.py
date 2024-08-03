class ServerArguments:

    def __init__(self, args, api):
        self.__source = {}
        self.__host = self.__get_setting('host', args, api)
        self.__port = self.__get_setting('port', args, api)
        self.__reload = self.__get_setting('reload', args, api)
        self.__verbose = self.__get_setting('verbose', args, api)
        self.__timeout = api.timeout
        self.__openapi_validate_request = api.openapi_validate_request
        self.__openapi_validate_response = api.openapi_validate_response
        self.__route = api.route

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def reload(self):
        return self.__reload

    @property
    def verbose(self):
        return self.__verbose

    @property
    def source(self):
        return self.__source

    @property
    def timeout(self):
        return self.__timeout

    @property
    def openapi_validate_request(self):
        return self.__openapi_validate_request

    @property
    def openapi_validate_response(self):
        return self.__openapi_validate_response

    def route(self, environ, server_response):
        return self.__route(environ, server_response)

    def __get_setting(self, key, args, api):
        if getattr(args, key):
            self.__source[key] = 'command-line'
            return getattr(args, key)
        self.__source[key] = 'api-settings'
        return getattr(api, key)
