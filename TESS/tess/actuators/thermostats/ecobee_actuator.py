from tess.actuators import BaseActuator
from tess.actuators.thermostats.ecobee.prisms_ecobee import PrismsEcobee
from tess.common.shared import throttle

from tess.common.const import *
from tess.common.shared import *


class EcobeeActuator(BaseActuator):
    
    def __init__(self, automation):
        
        #self.thermostats = actuator.thermostats
        #self.options = {'fan_on': self._fan_on,
        #                'fan_off': self._fan_off,
        #                'cool_temp': self._cool_temp,
        #                'heat_temp': self._heat_temp}

        super(EcobeeActuator, self).__init__(automation)

        self.ecobee = PrismsEcobee('Automation', self.automation.actuator_info, self.automation.db, self.automation.actuator_config_file)

        if not self.ecobee.authenticated:
            LOGGER.warn("Please enter the pin entry and will start in 2 minutes automatically")
            #isReady = input("Click Enter after pin entry")
            #time.sleep(120)
        
            self.ecobee.request_tokens()

        self._fan_mode = None
        self._hvac_mode = None
        self._hold_action = None
        self._equipment_status = None
        self._occupancy = None
        self._desired_heat = None
        self._desired_cool = None

    @property
    def fan_mode(self):
        return self._fan_mode

    @property
    def hvac_mode(self):
        return self._hvac_mode

    @property
    def hold_action(self):
        return self._hold_action

    @property
    def equipment_status(self):
        return self._equipment_status

    @property
    def occupancy(self):
        return self._occupancy

    @property
    def desired_heat(self):
        return self._desired_heat

    @property
    def desired_cool(self):
        return self._desired_cool


    def change_settings(self, id, name, value):

        request = None


        if name == 'normal':
            # Reset the fan min on minute to zero in case if the fan min on is set to something else
            request = self.ecobee.set_fan_min_on_time(id, str(0))
            # In order to off fan, the ecobee only allows the system to be off and then fan off.
            # Instead of just offing system in case the weather is cold and users want heat on, 
            # we shouldn't turn off the system.
            # Just resume the system
            request = self.ecobee.turn_fan_off(id, self._desired_cool, self._desired_heat,
                                     'indefinite', 0)
            ''' possible hvac modes are auto, auxHeatOnly, cool, heat, off '''
            request = self.ecobee.set_hvac_mode(id, self._hvac_mode)
            # put the original thermostate mode back
            request = self.ecobee.resume_program(id)

        if name == 'normal_with_datetime':
            # Reset the fan min on minute to zero in case if the fan min on is set to something else
            request = self.ecobee.set_fan_min_on_time(id, str(0))
            # In order to off fan, the ecobee only allows the system to be off and then fan off.
            # Instead of just offing system in case the weather is cold and users want heat on, 
            # we shouldn't turn off the system.
            # Just resume the system
            request = self.ecobee.turn_fan_off(id, self._desired_cool, self._desired_heat,
                                     'dateTime', value)
            ''' possible hvac modes are auto, auxHeatOnly, cool, heat, off '''
            request = self.ecobee.set_hvac_mode(id, self._hvac_mode)
            # put the original thermostate mode back
            request = self.ecobee.resume_program(id)


        # fan on
        if name == 'on':
            # Reset the fan min on minute to zero in case if the fan min on is set to something else
            request = self.ecobee.set_fan_min_on_time(id, str(0))

            request = self.ecobee.turn_fan_on(id, self._desired_cool, self._desired_heat,
                                     'indefinite', 0)

        if name == 'on_with_datetime':
            # Reset the fan min on minute to zero in case if the fan min on is set to something else
            request = self.ecobee.set_fan_min_on_time(id, str(0))

            request = self.ecobee.turn_fan_on(id, self._desired_cool, self._desired_heat,
                                     'dateTime', value)

        # runtime
        if name == 'runtime':
            request = self.ecobee.resume_program(id)

            request = self.ecobee.set_fan_min_on_time(id, value)

        # rule
        if name == 'rule':
            # Reset the fan min on minute to zero in case if the fan min on is set to something else
            request = self.ecobee.set_fan_min_on_time(id, value)


        # resume
        if name == 'resume':
            request = self.ecobee.set_fan_min_on_time(id, str(0))

            request = self.ecobee.resume_program(id)


        return request



    @throttle(limit=1, seconds=MIN_TIME_BETWEEN_UPDATES)
    def _update_thermostats(self):
        try:
            self.ecobee.get_thermostats()
        except StateUpdateException as e:
            LOGGER.error(e)


    @throttle(limit=1, seconds=MIN_TIME_BETWEEN_UPDATES)
    def refresh_settings(self, id):
        try:
            LOGGER.info("Updating the current state variables")

            self._update_thermostats()
        
            self._hvac_mode = self.ecobee.get_hvac_mode(id)
            self._fan_mode = self.ecobee.get_desired_fanmode(id)
            self._hold_action = self.ecobee.get_hold_action(id)
            self._equipment_status = self.ecobee.get_thermostat_data(id, 'equipmentStatus')
            self._occupancy = self.ecobee.get_occupancy(id)
            self._desired_cool, self._desired_heat = self.ecobee.get_desired_cool_heat(id)
            self._desired_cool = int(self._desired_cool / 10)
            self._desired_heat = int(self._desired_heat / 10)
        
            LOGGER.info("Done with updating")

        except Exception as e:
            LOGGER.error("An exception ocurred in {}: {}".format(sys._getframe().f_code.co_name, e))


    def read_settings(self, id, name):
        
        self.refresh_settings(id)

        # hvac mode
        value = None
        if name == 'havc_mode':
            return self.hvac_mode

        # desired fan mode
        if name == 'desired_fan_mode':
            return self.fan_mode
        
        # hold action
        if name == 'hold_action':
            return self.hold_action

        # equipment status
        if name == 'equipment_status':
            return self.equipment_status

        # occupancy
        if name == 'occupancy':
            return self.occupancy

        # desired cool
        if name == 'desired_cool':
            return self.desired_cool

        # desired heat
        if name == 'desired_heat':
            return self.desired_heat
        

    def get_actuator_summary_data(self, id, class_name):
        data = 'home_id:{}, class:{}, ecobee_id: {}, hvac_mode: {}, ' \
                'fan: {}, hold_action: {}, desired_cool: {}, ' \
                'desired_heat: {}, equipmentStatus: {}'.format(
                self.automation.actuator_info['home_id'], 
                class_name, 
                id, 
                self.hvac_mode, 
                self.fan_mode, 
                self.hold_action, 
                self.desired_cool, 
                self.desired_heat,
                self.equipment_status
                )
        
        return data


