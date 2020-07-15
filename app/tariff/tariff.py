from abc import ABC, abstractmethod
import time

class TariffException(Exception):
    pass


class Tariff(ABC):
    @abstractmethod
    def load(self, file):
        pass

    @abstractmethod
    def get_params(self):
        pass

    def get_param(self, param):
        return self.get_params()[param]

    def get_formula(self):
        return self.get_param('formula')


class TariffContainer:
    def __init__(self):
        self.tariffs = dict()

    def add(self, tariff_type, tariff: Tariff, t=time.time()):
        if tariff_type not in self.tariffs:
            self.tariffs[tariff_type] = dict()
        self.tariffs[tariff_type][t] = tariff

    def get(self, tariff_type, t=time.time()):
        try:
            times = list(self.tariffs[tariff_type].keys())
            times.sort()
            i = 0
            while i < len(times) and times[i] <= t:
                i += 1
            return self.tariffs[tariff_type][times[i-1]]
        except KeyError:
            raise TariffException('Please specify a valid tariff')
