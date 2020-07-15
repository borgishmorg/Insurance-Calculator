import logger
from request import request_handler, base_request_checker
import auth


def refresh_handler(request):
    logger.Logger().log(f'Get refresh from {request.hostname}:{request.port}')
    req_handler = request_handler.RequestHandler(request, base_request_checker.BaseRequestChecker(request))

    jwt_access_token = auth.get_access_token(req_handler.get_login())

    res = {
        'access-token': jwt_access_token
    }
    logger.Logger().log(f'Response {res} to {request.hostname}:{request.port}')
    return req_handler.response(**res)
