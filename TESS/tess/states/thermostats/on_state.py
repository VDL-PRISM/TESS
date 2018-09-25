import string, sys
import logging
import requests
import time
import threading
import socket

from tess.states import BaseState

from tess.common.const import *
from tess.common.shared import *


LOGGER = logging.getLogger()
#LOGGER = logging.getLogger('root')

hostname = socket.gethostname()


class OnState(BaseState):
    def __init__(self, automation):
        super().__init__(automation)


    def update(self):
        LOGGER.info("Fan On State: On State")
        next_state = self

        try:
            self.automation.actuator_handler.refresh_settings(self.actuator_id)

            if "fan" in self.automation.actuator_handler.equipment_status or self.automation.actuator_handler.actuator_mode == ACTUATOR_MODE_ON:
                pass
            else:
                next_state = next((x for x in self.automation.states if x.mode == 'off'), None)

                # Set the triggered to true to not to record again
                next_state.actuator_triggered = True

                LOGGER.info("Fan On State: Transition to Off")

        except StateUpdateException as e:
            LOGGER.error(e)

        return next_state


    def check(self):
        LOGGER.info("Fan On State: Entering")

        # Refresh the current thermostats so that we have the latest status of them.
        #self.update_current_state_variables(self.ecobee_id)

        ########## Call Base function ########
        #if super(OnState, self).is_safe() == False:
        #    # Failed the check condition. Don't run fan automation
        #    return False
        ######################################

        # If user sets the thermostat mode to off, don't run rules. They might want to stop everything...
        #if HVAC_MODE_OFF in self.hvac_mode:
        #    return

        ################ Uncomment below if we want to keep the user's setting #################
        # Do not interrupt normal operation of thermostat. If the current owner of the house has a setting to turn on heater, keep it that way.
        # No rules apply and just return
        if any(x in self.automation.actuator_handler.equipment_status for x in THERMOSTAT_NORMAL_OP):
            return
        ########################################################################################

        #for rule in (r for r in self.rules if r.active == 1 and r.actuator_mode in (ACTUATOR_MODE_OFF, ACTUATOR_MODE_AUTO)):
        LOGGER.info("Fan On State: Checking rules")
        for rule in (r for r in self.rules if r.active == 1 and r.actuator_mode in (ACTUATOR_MODE_AUTO)):
            try:

                time, data = self.automation.db.get_latest(rule.type, rule.query)

                if data == -1: continue

                # Uncomment the following code to use a percentile value as a below value to turn off
                #if rule.type == "query":
                #    time2, query_value = self.automation.db.get_latest(rule.type, rule.below_query)
                #    rule.below = query_value

                #if rule.type == "query":
                #    result = self.automation.db.get_data(rule.type, rule.below_query)

                #    query_value = self.get_percentile(result)
                #    rule.below = query_value


                LOGGER.info("Checking if %s meets rule %s", data, rule)
                if rule.check(data, self.automation.actuator_handler.occupancy):
                    LOGGER.info("Rule condition was met. Sending notification.")
                
                    try:
                        request = None

                        if rule.actuator_mode == ACTUATOR_MODE_OFF:
                            
                            if rule.duration_minute == 0:
                                request = self.automation.actuator_handler.change_settings(self.actuator_id, 'normal', str(0))
                            else:
                                request = self.automation.actuator_handler.change_settings(self.actuator_id, 'normal_with_datetime', rule.duration_minute)

                            #if rule.duration_minute == 0:
                            #    request = self.actuator_off(rule.ecobee_id, self.desired_cool, self.desired_heat)
                            #else:
                            #    request = self.actuator_off(rule.ecobee_id, self.desired_cool, self.desired_heat, 'dateTime', rule.duration_minute)

                            if request is not None:
                                if request.status_code == requests.codes.ok:
                                    self.automation.analysis_handler.db_record_rule_data(rule, data)
                            return

                        if rule.actuator_mode == ACTUATOR_MODE_AUTO:
                            request = self.automation.actuator_handler.change_settings(self.actuator_id, 'resume', '')

                            #request = self.actuator_resume(rule.ecobee_id)
                            if request is not None:
                                if request.status_code == requests.codes.ok:
                                    self.automation.analysis_handler.db_record_rule_data(rule, data)
                            return

                    except NotificationException as e:
                        LOGGER.error("Error occurred while sending notification: %s", e)
                else:
                    LOGGER.info("Rule condition was not met.")

            except DatabaseException as e:
                LOGGER.error(e)
        
        LOGGER.info("Fan On State: Exiting")


    def exit(self):
        pass