import logging
import socket

from tess.conditions import BaseCondition
from tess.common.const import *
from tess.common.shared import *


LOGGER = logging.getLogger()
#LOGGER = logging.getLogger('root')


class ThermostatBaseCondition(BaseCondition):

    def __init__(self, automation):
        """Initialize state object

        Args:
          state_name ([str]): state name as a string being used for state object initialization
        """
        super().__init__(automation)

        self.stopped = False

        LOGGER.info("Initializing Thermostat BaseCondition object")


    def exit(self):

        self.automation.analysis_handler.calc_stats()

        self.stopped = True
        self.is_running = False


    def is_safe(self):
        """Called to check if an emergency stutdown should happen 
            based on rules
        """
        can_run = True

        ###### Fan Shutdown Emergency Check #########
        for rule in (r for r in self.automation.rules if r.active == 1 and r.actuator_mode in (ACTUATOR_MODE_SHUTDOWN)):
            try:
                time, data = self.automation.db.get_latest(rule.type, rule.query)

                LOGGER.info("Checking if %s meets rule %s", data, rule)
                if rule.check(data, self.automation.actuator_handler.occupancy):

                    LOGGER.info("Rule condition was met. Sending notification.")
                
                    try:
                        request = self.automation.actuator_handler.change_settings(self.actuator_id, 'normal', str(0))
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


