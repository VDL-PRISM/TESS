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


class OffState(BaseState):
    def __init__(self, automation):
        super().__init__(automation)

    #def get_percentile(self, result):
    #    smallpms = [i['value'] for i in result]
    #    percentile = np.percentile(smallpms, 80)

    #    filterpms = [x for x in smallpms if x < percentile]
    #    #filterpms = smallpms[smallpms < percentile]
    #    mean = np.mean(filterpms)
    #    std = np.std(filterpms)

    #    return 2000

    def update(self):
        LOGGER.info("Fan Off State: Off State")
        next_state = self

        try:
            self.automation.actuator_handler.refresh_settings(self.actuator_id)

            if "fan" in self.automation.actuator_handler.equipment_status or self.automation.actuator_handler.actuator_mode == ACTUATOR_MODE_ON:
                
                next_state = next((x for x in self.automation.states if x.mode == 'on'), None)

                # Set the triggered to true to not to record again
                next_state.actuator_triggered = True

                LOGGER.info("Fan Off State: Transition to On")
            else:
                pass

        except StateUpdateException as e:
            LOGGER.error(e)         

        return next_state


    def check(self):
        LOGGER.info("Fan Off State: Entering")

        ## Refresh the current thermostats so that we have the latest status of them.
        #self.update_current_state_variables(self.ecobee_id)

        ########## Call Base function ########
        #if super(OffState, self).is_safe() == False:
        #    # Failed the check condition. Don't run fan automation
        #    return False
        ######################################

        ####### Fan Shutdown Emergency Check #########
        #for rule in (r for r in self.rules if r.active == 1 and r.actuator_mode in (ACTUATOR_MODE_SHUTDOWN)):
        #    try:
        #        time, data = self.automation.db.get_latest(rule.type, rule.query)

        #        LOGGER.info("Checking if %s meets rule %s", data, rule)
        #        if rule.check(data, self.occupancy):
        #            LOGGER.info("Rule condition was met. Sending notification.")
                
        #            try:
        #                request = None

        #                request = self.actuator_off(rule.ecobee_id, self.desired_cool, self.desired_heat)
        #                if request is not None:
        #                    if request.status_code == requests.codes.ok:
        #                        self.automation.analysis_handler.db_record_rule_data(rule, data)
        #                    #else:
        #                    #    raise NotificationException("The notification was not sent: {}".format(request['error']))

        #                return
                        
        #            except NotificationException as e:
        #                LOGGER.error("Error occurred while sending notification: %s", e)
        #        else:
        #            LOGGER.info("Rule condition was not met.")

        #    except DatabaseException as e:
        #        LOGGER.error(e)
        ####################################################

        # If user sets the thermostat mode to off, don't run rules. They might want to stop everything...
        #if HVAC_MODE_OFF in self.hvac_mode:
        #    return

        ############ Uncomment below if we don't want to override user's setting ####
        #if any(x in self.equipment_status for x in THERMOSTAT_NORMAL_OP):
        #    return
        #############################################################################

        #for rule in (r for r in self.rules if r.active == 1 and r.actuator_mode in (ACTUATOR_MODE_ON, ACTUATOR_MODE_AUTO)):
        LOGGER.info("Fan Off State: Checking rules")
        for rule in (r for r in self.rules if r.active == 1 and r.actuator_mode in (ACTUATOR_MODE_ON)):
            try:
                time, data = self.automation.db.get_latest(rule.type, rule.query)
                if data == -1: continue

                ## Temperature
                #ttime, tdata = self.automation.db.get_latest(rule.type, rule.tquery)
                #if tdata is not None and tdata > 212: # Temperature is higher than 100 degree C, something could be wrong

                #    return

                # Uncomment the following code to use a percentile above value
                #if rule.type == "query":
                #    time2, query_value = self.automation.db.get_latest(rule.type, rule.above_query)
                #    rule.above = query_value

                #if rule.type == "query":
                #    result = self.automation.db.get_data(rule.type, rule.above_query)
                #    query_value = self.get_percentile(result)
                #    rule.above = query_value

                LOGGER.info("Checking if %s meets rule %s", data, rule)
                if rule.check(data, self.occupancy):
                    LOGGER.info("Rule condition was met. Sending notification.")
                
                    try:
                        request = None

                        if rule.actuator_mode == ACTUATOR_MODE_ON:

                            if rule.duration_minute == 0:
                                request = self.automation.actuator_handler.change_settings(self.actuator_id, 'on', str(0))
                            else:
                                request = self.automation.actuator_handler.change_settings(self.actuator_id, 'on_with_datetime', rule.duration_minute)


                            #if rule.duration_minute == 0: #run indefinitely until the next rule is run 
                            #    request = self.actuator_on(rule.ecobee_id, self.desired_cool, self.desired_heat)
                            #else:
                            #    request = self.actuator_on(rule.ecobee_id, self.desired_cool, self.desired_heat, 'dateTime', rule.duration_minute)

                            if request is not None:
                                if request.status_code == requests.codes.ok:
                                    self.automation.analysis_handler.db_record_rule_data(rule, data)
                                #else:
                                #    raise NotificationException("The notification was not sent: {}".format(request['error']))

                            return
                        
                    except NotificationException as e:
                        LOGGER.error("Error occurred while sending notification: %s", e)
                else:
                    LOGGER.info("Rule condition was not met.")

            except DatabaseException as e:
                LOGGER.error(e)

        LOGGER.info("Fan Off State: Exiting")


    def exit(self):
        pass