#import click
import signal
import time
import schedule
import random
import logging
import logging.config

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from tess.automations import TESSAutomation
from tess.common.rule import Rule
from tess.helpers import helper
from tess.common.state import State
from tess.common.notification import Notification
from tess.common.condition import Condition

NETWORK = None

LOGGER = logging.getLogger()

class TESSController(TESSAutomation):

    """
    Baseclass for all TESS Controllers.  
    Control and automate the start thermostat for the fan operation.

    Must be run as a service class.
    """

    def __init__(self, rule_config_file):
        """Initialize a monitor object."""

        super().__init__(rule_config_file)
        
        self.actuator_info = self.config['actuator_handler']

        self.actuator_config_file = self.actuator_info['controller_config_file']

        # Load actuator module and class information from the rule.yaml file 
        # to construct an actuator object
        self.actuator_handler = helper.class_from_name(
            self.actuator_info['modulename'], 
            self.actuator_info['classname'], 
            self
            )

        # Create a notification engine that notifies who/whatever want to hear
        self.notify = Notification(self.actuator_handler)


        # Create an analysis handler for calculating stats by loading module and class dynamically
        self.analysis_handler = helper.class_from_name(
            self.config['analysis_handler']['modulename'], 
            self.config['analysis_handler']['classname'], 
            self
            )

        # Tables are dynamically generated if they don't exist in the database.
        # This allows to run different types of experiments while not overwriting other data
        self.analysis_table = self.config['analysis_handler']['analysis_table']
        self.data_table = self.config['analysis_handler']['data_table']
        self.experiment_table = self.config['analysis_handler']['experiment_table']


        # Create conditions that are to be scheduled for random experiments 
        self.states = State.create_states(self.config['states'], self)

        # Create policy based rules from rule configuration file.
        self.rules = Rule.create_rules(self.config['rules'])

        # Create conditions that are to be scheduled for random experiments 
        self.conditions = Condition.create_conditions(self.config['conditions'], self)


        self.current_condition = None
        self.thread_pool_executor = None



    def start(self):
        """ The external configuration file calls this function to 
        choose a random condition and submit it to executor to run the RCT.

        """
        LOGGER.info("\nI'm working ... at {0}".format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
        if self.current_condition != None:
            self.current_condition.exit()

        # Choose a randow condition now 
        self.current_condition = random.choice(self.conditions)

        LOGGER.info("{0} is selected randomly ... at {1}".format(self.current_condition, datetime.now().strftime('%Y/%m/%d %H:%M:%S')))

        # Check to see if the current condition is continusely running 
        is_running = self.current_condition.is_running()

        # If the selected condition is not running, then submit the condition now 
        while not is_running:
            LOGGER.info("{0} is not running yet and about to submit ... at {1}".format(self.current_condition, datetime.now().strftime('%Y/%m/%d %H:%M:%S')))

            thread1 = self.thread_pool_executor.submit(self.current_condition.run)

            LOGGER.info("\n{0} was submitted and about to sleep ... at {1}".format(self.current_condition, datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
            time.sleep(60)

            # Check again to see if the submitted condition is running now.
            is_running = self.current_condition.is_running()



    def run(self):
        """ The entry function that the main calls to run the automation RCT
        """

        def stop_running(sig_num, frame):
            LOGGER.debug("Shutting down the Actuator controller")
            self.RUNNING = False

        signal.signal(signal.SIGTERM, stop_running)
        signal.signal(signal.SIGINT, stop_running)        


        # Initialize the experiment states
        LOGGER.info("Running the TESS Actuator controller in schedule ...")
        """
        2. Initialize the conditions and fan states.
        SmartAir, SmartLight, SmartSleep have their own states. 
        """
        # Create a random condition executor process, 
        #Create how many workers we will run for this random process
        self.current_condition = None
        self.thread_pool_executor = ThreadPoolExecutor(max_workers=2)


        ############# Run a random condition now? Then uncomment the following ########### 
        # The scheduler will schedule a condition for the future, but won't run now. So, the statement below will pick a random condition and run it now
        # If a condition needs to be schedule at the next time, comment the following code
        LOGGER.info("Run a random condition now...")
        self.start()
        ########################


        # Schedule to run a random condition every ? - Grab the schedule statement and exec from the config file
        LOGGER.info("Schedule a random condition now ...")
        schedule_handler = self.config['schedule_handler']['statement']
        exec(schedule_handler)


        # Run while the experiment is configured
        while self.RUNNING:
            schedule.run_pending()
            time.sleep(1)


