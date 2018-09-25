import sys
import logging
import requests
import time
import socket

from tess.states import BaseState
from tess.common.const import *
from tess.common.shared import *


LOGGER = logging.getLogger()
#LOGGER = logging.getLogger('root')

hostname = socket.gethostname()


class ThermostatState(BaseState):
    def __init__(self, automation):
        super().__init__(automation)

    def is_safe(self):
        can_run = True

        # Refresh the current thermostats so that we have the latest status of them.
        self.automation.actuator_handler.refresh_settings(self.actuator_id)

        ###### Fan Shutdown Emergency Check #########
        for rule in (r for r in self.automation.rules if r.active == 1 and r.actuator_mode in (ACTUATOR_MODE_SHUTDOWN)):
            try:
                time, data = self.automation.db.get_latest(rule.type, rule.query)

                LOGGER.info("Checking if %s meets rule %s", data, rule)
                if rule.check(data, self.occupancy):

                    LOGGER.info("Rule condition was met. Sending notification.")
                
                    try:
                        request = None

                        request = self.actuator_off(rule.ecobee_id, self.desired_cool, self.desired_heat)
                        if request is not None:
                            if request.status_code == requests.codes.ok:
                                self.automation.analysis_handler.db_record_rule_data(rule, data)
                            #else:
                            #    raise NotificationException("The notification was not sent: {}".format(request['error']))

                    except NotificationException as e:
                        LOGGER.error("Error occurred while sending notification: %s", e)

                    can_run = False

                    tags = {'home_id':self.automation.ecobee_info['home_id']}
                    values = {'random': 'Shutdown'}
                    self.automation.analysis_handler.db_record_event_tags_fields(self.automation.experiment_table, tags, values)

                    #sys.exit() # EMERGENCY SHUTDOWN !!!!

                else:
                    LOGGER.info("Rule condition was not met.")

            except DatabaseException as e:
                LOGGER.error(e)

        return can_run
        ###################################################

