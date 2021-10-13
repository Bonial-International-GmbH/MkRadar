from abc import abstractmethod, ABC


class Provider(ABC):
    ''' Abstract classs all provider have to athear to'''
    protocol = None
    identifier = None

    @classmethod
    @abstractmethod
    def can_open(cls, url: str) -> bool:
        pass

    @classmethod
    @abstractmethod
    def get_page(cls, url: str) -> str:
        pass
