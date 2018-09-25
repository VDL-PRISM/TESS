import logging
import socket

from tess.common.const import *
from tess.common.shared import *


LOGGER = logging.getLogger()
#LOGGER = logging.getLogger('root')


class BaseCondition(object):

    def __init__(self, automation):
        """Initialize state object

        Args:
          state_name ([str]): state name as a string being used for state object initialization
        """
        LOGGER.info("Initializing BaseCondition object")

        self.automation = automation

        self.home_id = self.automation.actuator_info['home_id']
        self.actuator_id = self.automation.actuator_info['actuator_id']

        self._is_running = False
        self._stopped = False


    @property
    def stopped(self):
        return self._stopped

    @stopped.setter
    def stopped(self, value):
        self._stopped= value

    @property
    def is_running(self):
        return self._is_running

    @is_running.setter
    def is_running(self, value):
        self._is_running= value



    def is_safe(self):
        """Called to check if an emergency stutdown should happen 
            based on rules
        """
        pass
        ###################################################

    def run(self, state_name):
        """Called with each sensor measurement period

        Args:
          state_name ([str]): state name as a string being used for check rules
        """
        pass


    def exit(self):
        """Called when the experiment ends.
            Before exiting the state, add a new data point using analysis object
        """
        pass


    def change_settings(self, id, name, value):
        pass




