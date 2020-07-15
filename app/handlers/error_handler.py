import logger
from tariff.tariff import TariffException
from request.request_checker import RequestCheckError
from currency import CurrencyConvertException


def error_handler(request, exception):
    res = {
        'error': exception.__str__()
    }
    logger.Logger().log(f'Response {res} to {request.hostname}:{request.port}')
    return request.Response(json=res)


def add_error_handler(app):
    app.add_error_handler(TariffException, error_handler)
    app.add_error_handler(RequestCheckError, error_handler)
    app.add_error_handler(CurrencyConvertException, error_handler)
