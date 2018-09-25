#import click
import logging
from datetime import datetime

from tess.common.const import *
from tess.common.shared import *
import tess.helpers.helper as helper

LOGGER = logging.getLogger()


class Condition:
    """
    Represent random conditions for the controller to execute
    """
    def __init__(self, automation, name, mode, modulename, classname, active=1):
        self.name = name
        self.mode = mode
        self.active = active
        self.condition = helper.class_from_name(modulename, classname, automation)

    def exit(self):
        if self.condition != None:
            self.condition.exit()

    def stopped(self):
        if self.condition != None:
            return self.condition.stopped

        return False

    def is_running(self):
        if self.condition != None:
            return self.condition.is_running

        return False

    def run(self):
        LOGGER.debug("name: %s, mode: %s, time: %s", self.name, self.mode, datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        try:
            self.condition.run()
        except Exception as ex:
            LOGGER.error("Error occurred: %s", ex)


    @staticmethod
    def create_conditions(conditions, automation):
        return [Condition(automation, **condition) for condition in conditions if condition['active'] == 1]

    def __repr__(self):
        return '<Condition name={} active={}>'.format(self.name, self.active)

    def __str__(self):
        return '<Condition name={} active={}>'.format(self.name, self.active)

