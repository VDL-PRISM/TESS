import logging

LOGGER = logging.getLogger()

class Rule:
    def __init__(self, type, sensor, name, query, actuator_id, actuator_mode, when_occupied, duration_minute=0, max_trigger_attempts=1, active=1, above_query=None, above=None, below_query=None, below=None, notifications=None):
        self.type = type
        self.sensor = dict([(key,d[key]) for d in sensor for key in d])
        self.name = name
        self.query = query.format(**self.sensor)
        #self.query = query.format(*(sensor.split(",")))
        #self.tquery = "SELECT MEAN(value) FROM \"�F\" WHERE \"entity_id\"='{}_temperature' and time > now() - 2m".format(*(sensor.split(","))) # temperature query
        #self.hquery = "SELECT MEAN(value) FROM \"%\" WHERE \"entity_id\"='{}_humidity' and time > now() - 2m".format(*(sensor.split(","))) # humidity query

        self.actuator_id = actuator_id
        self.actuator_mode = actuator_mode
        self.when_occupied = when_occupied
        self.duration_minute = duration_minute
        self.max_trigger_attempts = max_trigger_attempts
        self.active = active

        self.above_query = above_query
        self.above = int(above) if above is not None else None
    
        self.below_query = below_query
        self.below = int(below) if below is not None else None
        #self.notifications = Notify.create_notifications(notifications)
        self.triggered = 0

    def check(self, value, when_occupied):
        trigger = self._check(value, when_occupied)

        if trigger and self.max_trigger_attempts != -1 and self.triggered > self.max_trigger_attempts:
            LOGGER.debug("Rule has already been triggered before.")
            return False

        LOGGER.debug("trigger: %s, triggered: %s", trigger, self.triggered)
        self.triggered += 1
        return trigger

    def _check(self, value, when_occupied):

        #######################################################
        # TURN OFF for experiment, the occupancy is not included 
        #condition = True

        # TURN ON for experiment, the occupancy is included 
        condition = False
        if self.when_occupied is None:
            # true, don't care
            condition = True
        else:
            if self.when_occupied == when_occupied:
                condition = True
            else:
                condition = False
        #######################################################

        if self.above and self.below:
            return self.above < value < self.below and condition

        if self.above:
            return self.above < value and condition

        if self.below:
            return value < self.below and condition

        raise Exception("Above and/or below must not be None.")

    @staticmethod
    def create_rules(rules):
        return [Rule(**rule) for rule in rules if rule['active'] == 1]

    def __repr__(self):
        return '<Rule above={} below={}>'.format(self.above, self.below)

    def __str__(self):
        return '<Rule above={} below={}>'.format(self.above, self.below)



