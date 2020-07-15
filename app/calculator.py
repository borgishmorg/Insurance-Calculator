from tariff import tariff
import currency
import re
import decimal


def _parse_arguments(s):
    openers = "{[\"'("
    closers = "}]\"')"
    state = []
    current = ""
    for c in s:
        if c == "," and not state:
            yield current
            current = ""
        else:
            current += c
            if c in openers:
                state.append(c)
            elif c in closers:
                state.pop(-1)
    yield current


def _multiply(*args):
    res = decimal.Decimal(1)
    for v in args:
        res *= decimal.Decimal(v)
    return res


class Calculator:
    def __init__(self, req_handler, tariff):
        self.request_handler = req_handler
        self.tariff = tariff
        self.tariff_params = self.tariff.get_params()
        self.request_params = self.request_handler.get_params()
        self.variables = dict()

    def _value(self, value):
        if value in self.variables:
            return self.variables[value]
        elif value in self.tariff_params:
            return self.tariff_params[value]
        elif value in self.request_params:
            return self.request_params[value]
        raise tariff.TariffException(f'{value} is not specified')

    def _interpret_list(self, cmd):
        func = cmd[0]
        args = list()
        for c in cmd[1:]:
            args.append(self._interpret(c))
        try:
            if func == 'multiply':
                return _multiply(*args)
            elif func == 'bigger':
                return args[0] > args[1]
            elif func == 'equal':
                return args[0] == args[1]
            elif func == 'and':
                return args[0] and args[1]
            elif func == 'or':
                return args[0] or args[1]
            elif func == 'max':
                return max(*args)
        except (TypeError, decimal.InvalidOperation):
            raise tariff.TariffException('Please specify a valid params types')

    def _interpret_string(self, cmd):
        cmd = cmd.strip()

        if cmd[0] == '$':
            return self._value(cmd[1:])

        match = re.fullmatch(r'([a-z]+)\((.*)\)', cmd)
        if match:
            func = match.group(1)
            args = _parse_arguments(match.group(2))
            return self._interpret([func, *args])
        elif '->' in cmd:
            lst = cmd.split('->')
            try:
                val = self._value(self._interpret(lst[0]))
            except (TypeError, KeyError):
                raise tariff.TariffException(f'{self._interpret(lst[0])} is not available')
            for k in lst[1:]:
                try:
                    val = val[self._interpret(k)]
                except (TypeError, KeyError):
                    raise tariff.TariffException(f'{self._interpret(k)} is not available')
            return val
        try:
            return decimal.Decimal(cmd)
        except decimal.InvalidOperation:
            return cmd

    def _interpret(self, cmd):
        if type(cmd) is list:
            return self._interpret_list(cmd)
        elif type(cmd) is str:
            return self._interpret_string(cmd)
        return cmd

    def calc(self):
        for name, cmd in self.tariff.get_formula().items():
            try:
                ok = self._interpret(cmd['condition'])
            except (tariff.TariffException, KeyError):
                ok = False
            if name == 'default' or ok:
                minimum = decimal.Decimal(currency.convert('EUR', self._value('currency'), self._value('minimum_EUR')))
                cost = self._interpret(cmd['cost'])
                res = max(minimum, cost)
                res = res.quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_DOWN)
                return {'cost': int(res), 'currency': self._value('currency')}
        raise tariff.TariffException('Your request is not satisfy any condition')
