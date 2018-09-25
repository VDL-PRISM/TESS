class BaseState(object):
    """
    Base class for the actuator 

    Communicate to the Actuator API to control the operation.

    Keep the state of the actuator device.

    Record the current event to the TESS cloud server.
    """

    def __init__(self, automation):
        """Initialize state object

        Args:
          state_name ([str]): state name as a string being used for state object initialization
        """
        self.error_description = ''
        self.automation = automation

        #self.config = automation.config
        #self.db = automation.db
        #self.db = automation.db
        #self.rules = automation.rules
        #self.actuator_handler = automation.actuator_handler
        #self.actuator_info = automation.config['actuator_handler']

        # primary actuator id: users can have multiple actuators,
        # but this service is for one primary actuator for inital experiment and because of possible conflicts 
        self.home_id = self.automation.actuator_info['home_id']
        self.actuator_id = self.automation.actuator_info['actuator_id']
        self._actuator_mode = None
        self._actuator_value = 0

        self._actuator_triggered = False
        self._actuator_triggered_else = False

        self._is_running = False
        self._stopped = False

    @property
    def actuator_triggered(self):
        return self._actuator_triggered

    @actuator_triggered.setter
    def actuator_triggered(self, value):
        self._actuator_triggered = value

    @property
    def actuator_triggered_else(self):
        return self._actuator_triggered_else

    @actuator_triggered_else.setter
    def actuator_triggered_else(self, value):
        self._actuator_triggered_else = value

    @property
    def actuator_value(self):
        return self._actuator_value

    @actuator_value.setter
    def actuator_value(self, value):
        if value < 0 or value > 1:
            raise ValueError("Fan value below 0 or above 1 is not possible")
        self._actuator_value = value

    @property
    def stopped(self):
        return self._stopped

    @stopped.setter
    def stopped(self, value):
        self._stopped= value

    @property
    def is_running(self):
        return self._is_running

    @is_running.setter
    def is_running(self, value):
        self._is_running= value


    def state_check(self, state_name):
        """Called with each sensor measurement period

        Args:
          state_name ([str]): state name as a string being used for check rules
        """
        pass

    def state_exit(self):
        """Called when the experiment ends.
            Before exiting the state, add a new data point using analysis object
        """
        pass


