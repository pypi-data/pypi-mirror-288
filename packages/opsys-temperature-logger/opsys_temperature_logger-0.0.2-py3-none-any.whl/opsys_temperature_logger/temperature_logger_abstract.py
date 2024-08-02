from abc import ABC, abstractmethod


class TemperatureLoggerAbstract(ABC):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def read_temperature(self, channel: int):
        pass
    
    @abstractmethod
    def close_connection(self):
        pass
    