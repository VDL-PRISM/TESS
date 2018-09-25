from abc import ABCMeta, abstractmethod

class BaseActuator(object):
    __metaclass__ = ABCMeta

    def __init__(self, automation):
        self.automation = automation


    @abstractmethod
    def change_settings(self, id, name, value):
        pass


    @abstractmethod
    def read_settings(self, id, name):
        pass


