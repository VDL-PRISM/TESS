#import click
import yaml
import logging
import importlib
from abc import ABCMeta, abstractmethod

from tess.common.rule import Rule
from tess.common.state import State
from tess.common.condition import Condition

from tess.common.influx_database import Database
from tess.common.notification import Notification
from tess.helpers import helper

NETWORK = None

LOGGER = logging.getLogger()


class TESSAutomation:

    """
    Baseclass for all TESS Controllers.  
    Control and automate the start thermostat for the fan operation.

    Must be run as a service class.
    """
    
    def __init__(self, rule_config_file):
        """0. Initialize the controller class"""
        LOGGER.debug(rule_config_file)

        # Load experiment configuration file (e.g., SmartAir, SmartLight, SmartSleep)
        with open(rule_config_file, 'r', encoding='utf-8', errors='ignore') as stream:
            try:
                config = yaml.load(stream)
            except UnicodeDecodeError as exc:
                LOGGER.error("An exception occurred in {0}:{1}".format(self.__class__.__name__, exc))
            except yaml.YAMLError as exc:
                LOGGER.error("An exception occurred in {0}:{1}".format(self.__class__.__name__, exc))

        
        # keep the current state and move to the next state of ecobee depending on the state of the ecobee and conditions
        self.config = config
        #config = yaml.load(rule_config_file)

        # Create database connections (e.g., InfluxDB or Postgre DB)
        # Syntax of the database connection should be specific to each database
        # self.localdb = Database(**config['local_database'])
        self.db = Database(**config['tess_database'])
        self.actuator_info = config['actuator_handler']


        self.RUNNING = True


    @abstractmethod
    def run(self):
        pass



    @abstractmethod
    def start(self):
        pass