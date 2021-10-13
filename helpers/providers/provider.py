''' Contains the abstract class(interface) for providers '''
from abc import abstractmethod, ABC


class Provider(ABC):
    ''' Abstract classs all provider have to athear to'''
    protocol: str
    identifier: str

    @classmethod
    @abstractmethod
    def can_open(cls, url: str) -> bool:
        ''' Return true if the provider can handle the url'''

    @classmethod
    @abstractmethod
    def get_page(cls, url: str) -> str:
        ''' Returns the url content'''
