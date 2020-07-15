from abc import ABC, abstractmethod


class RequestCheckError(Exception):
    pass


class RequestChecker(ABC):
    @abstractmethod
    def check(self):
        pass
