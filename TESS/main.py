#import click
import logging
import logging.config
import yaml
import argparse

from tess.automations.tess_controller import TESSController
from tess.automations.tess_monitor import TESSMonitor

def main(process, rule_config_file, logging_config_file='logging_controller.yaml'):

    """Choose which process to run by accepting an argument."""
    if process == "monitor":
        logging.config.dictConfig(yaml.load(open(logging_config_file, 'r')))
        LOGGER = logging.getLogger(__name__)

        monitor = TESSMonitor(rule_config_file)
        monitor.run()

    elif process == "controller":
        logging.config.dictConfig(yaml.load(open(logging_config_file, 'r')))
        LOGGER = logging.getLogger(__name__)

        controller = TESSController(rule_config_file)
        controller.run()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Start automation process bassed on input arguments')
    parser.add_argument('process', help='Automation Type', choices=['monitor', 'controller'])
    parser.add_argument('rule_config_file', help='Rule configuration file, used to create other related objects ' + \
                        ' for running random experiments')
    parser.add_argument('logging_config_file', help='Logging configuration file that sets up a logger for its ' + \
                        'format and file')

    #args, unknown = parser.parse_args()
    args, unknown = parser.parse_known_args()

    main(args.process, args.rule_config_file, args.logging_config_file)




