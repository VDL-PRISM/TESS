import logging
from tess.common.shared import throttle
from tess.common.const import ACTUATOR_MODE_ON, ACTUATOR_MODE_OFF

LOGGER = logging.getLogger()

class Notification():
    def __init__(self, actuator_handler):
        self.actuator_handler = actuator_handler

    @throttle(limit=1, seconds=160)
    def send_notification(self, home_id, actuator_mode, actuator_id=0):
        # Send notification
        LOGGER.info("Sending notification")

        # Before sending a new command to the thermostat, check the current state and 
        # then send a new command if the current state and new state are different.

        if actuator_mode == ACTUATOR_MODE_ON:
            request = self.ecobee.turn_fan_on(actuator_id, 82, 69)
        elif actuator_mode == ACTUATOR_MODE_OFF:
            request = self.ecobee.turn_fan_off(actuator_id)
        else:
            raise Exception("Invalid actuator_handler mode")

        if request.status_code != requests.codes.ok:
            raise NotificationException("The notification was not sent: {}".format(request['error']))

        LOGGER.info("Sent a notification to %s, %s", home_id, self.actuator_handler[actuator_id]['name'])


