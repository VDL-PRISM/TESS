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
#LOGGER = logging.getLogger('root')

hostname = socket.gethostname()


class MonitorCondition(ThermostatBaseCondition):
    def __init__(self, automation):
        super().__init__(automation)

        self.actuator_value = None
        self.actuator_triggered = False
        self.actuator_triggered_else = False

    """
    Record the Fan On or Off state constantly.

    Update the current fan state by checking the fan mode 'fan' using the smart thermostat api
    """

    #@throttle(limit=1, seconds=MIN_TIME_BETWEEN_UPDATES)
    def run(self):

        try:
            LOGGER.info("Fan Monitor State: Only Monitor fan for ecobee thermostat")

            self.automation.actuator_handler.refresh_settings(self.actuator_id)

            LOGGER.debug("Updated current state variables")

            data = self.automation.actuator_handler.get_actuator_summary_data(self.actuator_id, self.__class__.__name__)

            LOGGER.debug("Created state data")

            if "fan" in self.automation.actuator_handler.equipment_status or self.automation.actuator_handler.actuator_mode == ACTUATOR_MODE_ON:
                data += ', actuator_on: 1'
                self.actuator_value = 1
                if not self.actuator_triggered:
                    LOGGER.debug("Fan on state notification")
                    self.automation.analysis_handler.db_record_home_data(self.home_id, data)
                    self.actuator_triggered = True
                    self.actuator_triggered_else = False
            else:
                data += ', actuator_on: 0'
                self.actuator_value = 0
                if not self.actuator_triggered_else:
                    LOGGER.debug("Fan off state notification")
                    self.automation.analysis_handler.db_record_home_data(self.home_id, data)
                    self.actuator_triggered_else = True
                    self.actuator_triggered = False


            tags = dict()
            tags['home_id'] = self.home_id
            tags['actuator_on'] = self.actuator_value
            tags['occupancy'] = self.automation.actuator_handler.occupancy

            values = dict()
            values['value'] = self.actuator_value
            values['state'] = data
            values['occupancy'] = self.automation.actuator_handler.occupancy

            self.automation.analysis_handler.db_record_event_tags_fields(self.automation.data_table, tags, values)
            LOGGER.debug("Notified state tags")

        except StateUpdateException as e:
            LOGGER.error(e)

