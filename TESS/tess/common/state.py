#import click
import logging
from datetime import datetime

from tess.common.const import *
from tess.common.shared import *
import tess.helpers.helper as helper

LOGGER = logging.getLogger()


class State:
    """
    Represent states for the actuator to execute
    """
    def __init__(self, automation, name, mode, modulename, classname, active=1):
        self.name = name
        self.mode = mode
        self.active = active
        self.state = helper.class_from_name(modulename, classname, automation)

    def update(self):
        if self.state != None:
            self.state.update()

    def check(self):
        if self.state != None:
            self.state.check()

    def exit(self):
        if self.state != None:
            self.state.exit()

    def stopped(self):
        if self.state != None:
            return self.state.stopped

        return False

    def is_running(self):
        if self.state != None:
            return self.state.is_running

        return False

    def run(self):
        LOGGER.debug("name: %s, mode: %s, time: %s", self.name, self.mode, datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        try:
            self.state.run()
        except Exception as ex:
            LOGGER.error("Error occurred: %s", ex)


    @staticmethod
    def create_states(states, automation):
        return [State(automation, **state) for state in states if state['active'] == 1]

    def __repr__(self):
        return '<State name={} mode={}>'.format(self.name, self.mode)

    def __str__(self):
        return '<State name={} mode={}>'.format(self.name, self.mode)

