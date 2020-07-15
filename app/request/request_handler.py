class RequestHandler:
    def __init__(self, request, checker):
        self.request = request
        self.login = checker.check()

        try:
            self.params = request.json
        except SystemError:
            self.params = dict()
        if self.params is None:
            self.params = dict()

    def get_params(self):
        return self.params

    def get_param(self, param):
        return self.params[param]

    def get_login(self):
        return self.login

    def response(self, **params):
        return self.request.Response(json=params)
