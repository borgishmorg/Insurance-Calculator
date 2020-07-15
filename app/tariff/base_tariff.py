from tariff import tariff
import json


class BaseTariff(tariff.Tariff):
    FILENAME = './app/tariff/base_tariff.json'

    def __init__(self, filename=FILENAME):
        self.params = dict()
        self.variables = dict()
        self.load(filename)

    def load(self, filename=FILENAME):
        with open(filename) as file:
            self.params = json.load(file)

    def get_params(self):
        return self.params
