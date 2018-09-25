from abc import ABCMeta, abstractmethod

class BaseAnalysis(object):
    __metaclass__ = ABCMeta

    def __init__(self, automation):
        self.automation = automation

    @abstractmethod
    def add_new_datapoint(self, name, value):
        # avg day of pm 2.5
        # sleep quality
        # total electric use over experimental period

        pass

    @abstractmethod
    def calc_stats(self, name):
        # code to evaluate change...
        # return p-value
        pass


