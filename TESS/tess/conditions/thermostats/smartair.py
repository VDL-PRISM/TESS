import string, sys
import logging
import requests
import time
import threading
import socket

from tess.conditions.thermostats import ThermostatBaseCondition

from tess.common.const import *
from tess.common.shared import *


LOGGER = logging.getLogger()
hostname = socket.gethostname()


class SmartAirCondition(ThermostatBaseCondition):
    def __init__(self, automation):
        super().__init__(automation)

        # Start with the off system behavior
        self.smart_state = next((x for x in self.automation.states if x.name == 'off'), None)
        #self.smart_state.update()


    def check(self):

        ######### Call Base function ########
        if super(SmartAirCondition, self).is_safe() == False:
            # Failed the check condition. Don't run fan automation
            return False
        #####################################

        self.smart_state.check()
        time.sleep(10)

        self.smart_state = self.smart_state.update()
        time.sleep(10)

    def run(self):
        self.stopped = False
        self.is_running = False

        LOGGER.info("Actuator Rule: turning on the actuator device")
        #self.update_current_state_variables(self.ecobee_id)

        ######### Call Base function ########
        if super(SmartAirCondition, self).is_safe() == False:
            # Failed the check condition. Don't run fan automation
            return False
        #####################################

        tags = {'home_id':self.home_id}
        values = {'random': 'Rule'}
        self.automation.analysis_handler.db_record_event_tags_fields(self.automation.experiment_table, tags, values)


        # Reset the fan min on minute to zero in case if the fan min on is set to something else
        request = self.automation.actuator_handler.change_settings(self.actuator_id, 'rule', str(0))


        data = self.automation.actuator_handler.get_actuator_summary_data(self.actuator_id, self.__class__.__name__)
        self.automation.analysis_handler.db_record_home_data(self.home_id, data)

        while not self.stopped:
            try:
                self.is_running = True
                if self.check() == False:
                    self.stopped = True
                    self.is_running = False

            except Exception as e:
                LOGGER.error(e)
                time.sleep(60)
                continue
