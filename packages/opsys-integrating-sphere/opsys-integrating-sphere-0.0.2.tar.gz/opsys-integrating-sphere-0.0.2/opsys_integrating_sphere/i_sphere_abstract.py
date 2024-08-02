from abc import ABC, abstractmethod


class ISphereAbstract(ABC):  
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
    
    @abstractmethod
    def get_optical_power(self):
        pass