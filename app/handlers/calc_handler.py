import logger
from request import request_handler, base_request_checker
from tariff import tariffs
import calculator


def calc_handler(request):
    logger.Logger().log(f'Get calc from {request.hostname}:{request.port}')

    req_handler = request_handler.RequestHandler(request, base_request_checker.BaseRequestChecker(request))

    if 'tariff' in req_handler.get_params():
        req_tariff = tariffs.tariff_container.get(req_handler.get_param('tariff'))
    else:
        req_tariff = tariffs.tariff_container.get('base')

    calc = calculator.Calculator(req_handler, req_tariff)
    res = calc.calc()
    logger.Logger().log(f'Response {res} to {request.hostname}:{request.port}')
    return req_handler.response(**res)
