import logging
import requests
import time
import socket

from tess.conditions.thermostats import ThermostatBaseCondition
from tess.common.const import *
from tess.common.shared import *


LOGGER = logging.getLogger()
#LOGGER = logging.getLogger('root')

hostname = socket.gethostname()




class Runtime20Condition(ThermostatBaseCondition):
    """
    This class is for running fan on for a certain time period every hour
    regardless of air quality sensor data. Blind random test to see if we can compare Fan runtime to Fan rule.
    """
    def check(self):
        ######### Call Base function ########
        if super(Runtime20Condition, self).is_safe() == False:
            # Failed the check condition. Don't run fan automation
            return False
        #####################################

        time.sleep(60)


    def run(self):
        self.stopped = False
        self.is_running = False

        LOGGER.info("Fan Runtime Condition: setting fan runtime for ecobee thermostat")

        # Refresh the current thermostats so that we have the latest status of them.
        #self.update_current_state_variables(self.ecobee_id)

        ######### Call Base function ########
        if super(Runtime20Condition, self).is_safe() == False:
            # Failed the check condition. Don't run fan automation
            return False
        #####################################


        # If user sets the thermostat mode to off, don't run rules. They might want to stop everything...
        #if HVAC_MODE_OFF in self.hvac_mode:
        #    return

        # Do not interrupt normal operation of thermostat. If the current owner of the house has a setting to turn on heater, keep it that way.
        # No rules apply and just return
        #if any(x in self.equipment_status for x in THERMOSTAT_NORMAL_OP):
        #    return

        runtime = 20
        #runtime = random.choice(self.automation.actuator_info['actuator_min_on_minutes_per_hour'])
        tags = {'home_id':self.home_id}
        values = {'random': 'Runtime', 'minutes': runtime}
        self.automation.analysis_handler.db_record_event_tags_fields(self.automation.experiment_table, tags, values)


        try:
            # set a new fan on min minute for random expe.
            request = self.automation.actuator_handler.change_settings(self.actuator_id, 'runtime', str(runtime))

            if request is not None:
                if request.status_code == requests.codes.ok:
                    self.is_running = True
                    data = self.automation.actuator_handler.get_actuator_summary_data(self.actuator_id, self.__class__.__name__)
                    self.automation.analysis_handler.db_record_home_data(self.home_id, data)
        except NotificationException as e:
            LOGGER.error("Error occurred while sending notification: %s", e)

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
