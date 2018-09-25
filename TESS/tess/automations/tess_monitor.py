import logging
import logging.config
import signal
import time


from tess.common.notification import Notification
import tess.helpers.helper as helper

from tess.automations import TESSAutomation
from tess.common.condition import Condition

NETWORK = None

LOGGER = logging.getLogger()

class TESSMonitor(TESSAutomation):

    """
    Baseclass for all TESS Monitors.  
    Monitor the smart thermostat state especially fan mode.

    Run monitoring service continuously
    """
    
    def __init__(self, rule_config_file):
        """Initialize a monitor object."""
        super().__init__(rule_config_file)

        # Create conditions that are to be scheduled for random experiments 
        self.monitor_conditions = Condition.create_conditions(self.config['monitor_conditions'], self)

        self.actuator_config_file = self.actuator_info['monitor_config_file']

        # Load actuator module and class information from the rule.yaml file 
        # to construct an actuator object
        self.actuator_handler = helper.class_from_name(
            self.actuator_info['modulename'], 
            self.actuator_info['classname'], 
            self
            )



    def run(self):
        """Run the monitoring now"""
        LOGGER.info("Running the TESS Ecobee Monitor ...")

        def stop_running(sig_num, frame):
            LOGGER.debug("Shutting down the ecobee monitoring")
            self.RUNNING = False

        signal.signal(signal.SIGTERM, stop_running)
        signal.signal(signal.SIGINT, stop_running)        

        self.current_condition = next((x for x in self.monitor_conditions if x.mode == 'monitor'), None)

        while self.RUNNING:
            try:
                # Monitor the thermostat fan operation status
                """Update the fan state every minute"""
                self.current_condition.run()
                time.sleep(60)

            except Exception as e:
                LOGGER.error("Exception occurred: %s", e)
                if not self.RUNNING:
                    LOGGER.debug("Stopping the monitor because RUNNING is false")
                
                time.sleep(60)
                continue

        LOGGER.debug("Exiting...")
