import users
import auth
import base64
import jwt

from request import request_checker

PATH_LOGIN = '/login'
PATH_REFRESH = '/refresh'
PATH_CALC = '/calc'


class BaseRequestChecker(request_checker.RequestChecker):
    def __init__(self, request):
        self.request = request
        self.auth = request.headers['Authorization'].split()[1] if 'Authorization' in request.headers else None

    def check(self):
        if self.request.path == PATH_LOGIN:
            return self.check_login_password()
        elif self.request.path == PATH_REFRESH:
            return self.check_refresh_token()
        elif self.request.path == PATH_CALC:
            return self.check_access_token()

    def check_login_password(self):
        if self.auth is None:
            raise request_checker.RequestCheckError('Please specify a valid login/password')

        decoded_auth = base64.b64decode(self.auth).decode().split(sep=':')

        if len(decoded_auth) != 2:
            raise request_checker.RequestCheckError('Please specify a valid login/password')

        login, password = decoded_auth
        if not (login in users.users and users.users[login] == password):
            raise request_checker.RequestCheckError('Please specify a valid login/password')
        return login

    def check_access_token(self):
        try:
            payload = jwt.decode(self.auth, auth.JWT_SECRET)
        except(jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise request_checker.RequestCheckError('Please specify a valid access token')
        else:
            if payload['type'] != 'access':
                raise request_checker.RequestCheckError('Please specify a valid access token')
        return payload['login']

    def check_refresh_token(self):
        try:
            payload = jwt.decode(self.auth, auth.JWT_SECRET)
        except(jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise request_checker.RequestCheckError('Please specify a valid refresh token')
        else:
            if payload['type'] != 'refresh':
                raise request_checker.RequestCheckError('Please specify a valid refresh token')
