from abc import ABCMeta, abstractmethod


class Messageable(metaclass=ABCMeta):

    @abstractmethod
    def _get_room(self):
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Messageable:
            ...
