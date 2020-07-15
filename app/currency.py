CURRENCIES = {
    'USD': {
        'USD': 1.,
        'EUR': 0.89,
        'RUB': 69.6
    },
    'EUR': {
        'USD': 1.12,
        'EUR': 1.,
        'RUB': 78.16
    },
    'RUB': {
        'USD': 0.014367816,
        'EUR': 0.012794268,
        'RUB': 1.
    }
}


class CurrencyConvertException(Exception):
    pass


def convert(fr, to, amount):
    try:
        return amount*CURRENCIES[fr][to]
    except KeyError:
        raise CurrencyConvertException('Please specify a valid currency')
