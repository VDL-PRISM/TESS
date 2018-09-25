import logging

from tess.analysis import BaseAnalysis
from tess.common.shared import DatabaseException

LOGGER = logging.getLogger()

class Analysis(BaseAnalysis):
    def __init__(self, automation):
        super().__init__(automation)

        self.home_id = self.automation.actuator_info['home_id']
        self.actuator_id = self.automation.actuator_info['actuator_id']

    def add_new_datapoint(self, name, value):
        # avg day of pm 2.5
        # sleep quality
        # total electric use over experimental period
        pass

    def calc_stats(self, name):
        # code to evaluate change...
        # Calculate an average value of PM2.5 for everyday and save it to analysis table
        query = ''
        time, data = self.automation.db.get_latest('query', rule.query)
        # return p-value
        pass


    def db_record_home_data(self, home_id, data):
        try:
            self.automation.db.record_event(home_id, data)
                                    
        except DatabaseException as e:
            LOGGER.error(e)

    def db_record_event_tags_fields(self, measurement, tags, fields):
        try:
            self.automation.db.record_event_tags(measurement, tags, fields)
                                    
        except DatabaseException as e:
            LOGGER.error(e)
            pass
        except Exception as e:
            LOGGER.error(e)
            pass

    def db_record_rule_data(self, rule, data):
        try:
            self.automation.db.record_event(
                self.home_id, 'home_id: {}, rulename: {}, ecobee_id: {}, fan: {}, duration: {} m, above: {}, below: {}, current: {}'.format(
                self.home_id, rule.name, rule.ecobee_id, rule.actuator_mode, rule.duration_minute, rule.above, rule.below, data))

        except DatabaseException as e:
            LOGGER.error(e)
    
