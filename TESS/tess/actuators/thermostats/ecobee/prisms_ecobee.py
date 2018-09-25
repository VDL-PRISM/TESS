from .pyecobee import Ecobee
import requests
import datetime
import logging

LOGGER = logging.getLogger()

ACTUATOR_MODE_ON = "on"
ACTUATOR_MODE_OFF = "off"
ACTUATOR_MODE_AUTO = "auto"
HVAC_MODE_OFF = "off"


class PrismsEcobee(Ecobee):
    def __init__(self, appname, ecobee_info, db, config_filename = None, api_key = None, config = None):
        super(PrismsEcobee, self).__init__(appname, ecobee_info, db, config_filename, api_key, config)
        self.appname = appname
        self.ecobee_info = ecobee_info
        self.db = db

    #def update(self):
    #    self.refresh_tokens()


    def turn_fan_on(self, index, cool_temp, heat_temp, 
                      hold_type="indefinite", duration_minute=0):
        ''' Set a hold and fan on without changing the temperature in home .
            Important not to change the user's temperature setting for heat or cold.
        '''
        fan_mode = 'on'
        hold_time = ""
        if hold_type == "dateTime":
            end_datetime = datetime.datetime.now() + datetime.timedelta(minutes = duration_minute)
            endDate = end_datetime.strftime("%Y-%m-%d")
            endTime = end_datetime.strftime("%H:%M:%S")
            hold_time = '","endDate":"' + endDate + '","endTime":"' + endTime

        url = 'https://api.ecobee.com/1/thermostat'
        header = {'Content-Type': 'application/json;charset=UTF-8',
                  'Authorization': 'Bearer ' + self.access_token}
        params = {'format': 'json'}
        body = ('{"functions":[{"type":"setHold","params":{"holdType":"' + hold_type + 
                '","coolHoldTemp":"' + str(cool_temp * 10) +
                '","heatHoldTemp":"' + str(heat_temp * 10) + 
                '","fan":"' + fan_mode + hold_time +
                '","isTemperatureAbsolute":false,"isTemperatureRelative":false}}],'
                '"selection":{"selectionType":"thermostats","selectionMatch"'
                ':"' + self.thermostats[index]['identifier'] + '"}}')
        request = requests.post(url, headers=header, params=params, data=body)
        if request.status_code == requests.codes.ok:
            return request
        else:
            LOGGER.warn("Error connecting to Ecobee while attempting to set"
                  " a hold and fan on.  Refreshing tokens...")
            self.refresh_tokens()

    #def turn_fan_on(self, index, cool_temp, heat_temp, 
    #                  hold_type="indefinite", duration_minute=0):
    #    ''' Set a hold and fan on '''
    #    fan_mode = 'on'
    #    hold_time = ""
    #    if hold_type == "dateTime":
    #        end_datetime = datetime.datetime.now() + datetime.timedelta(minutes = duration_minute)
    #        endDate = end_datetime.strftime("%Y-%m-%d")
    #        endTime = end_datetime.strftime("%H:%M:%S")
    #        hold_time = '","endDate":"' + endDate + '","endTime":"' + endTime

    #    url = 'https://api.ecobee.com/1/thermostat'
    #    header = {'Content-Type': 'application/json;charset=UTF-8',
    #              'Authorization': 'Bearer ' + self.access_token}
    #    params = {'format': 'json'}
    #    body = ('{"functions":[{"type":"setHold","params":{"holdType":"' + hold_type + 
    #            '","coolHoldTemp":"' + str(cool_temp * 10) +
    #            '","heatHoldTemp":"' + str(heat_temp * 10) + 
    #            '","fan":"' + fan_mode + hold_time +
    #            '"}}],'
    #            '"selection":{"selectionType":"thermostats","selectionMatch"'
    #            ':"' + self.thermostats[index]['identifier'] + '"}}')
    #    request = requests.post(url, headers=header, params=params, data=body)
    #    if request.status_code == requests.codes.ok:
    #        return request
    #    else:
    #        LOGGER.warn("Error connecting to Ecobee while attempting to set"
    #              " a hold and fan on.  Refreshing tokens...")
    #        self.refresh_tokens()

    def _turn_fan_off(self, index, cool_temp, heat_temp, 
                      hold_type="indefinite", duration_minute=0):
        ''' Set a hold and fan off '''
        fan_mode = 'auto'

        hold_time = ""
        if hold_type == "dateTime":
            end_datetime = datetime.datetime.now() + datetime.timedelta(minutes = duration_minute)
            endDate = end_datetime.strftime("%Y-%m-%d")
            endTime = end_datetime.strftime("%H:%M:%S")
            hold_time = '","endDate":"' + endDate + '","endTime":"' + endTime

        url = 'https://api.ecobee.com/1/thermostat'
        header = {'Content-Type': 'application/json;charset=UTF-8',
                  'Authorization': 'Bearer ' + self.access_token}
        params = {'format': 'json'}
        body = ('{"functions":[{"type":"setHold","params":{"holdType":"' + hold_type + 
                '","coolHoldTemp":"' + str(cool_temp * 10) +
                '","heatHoldTemp":"' + str(heat_temp * 10) + 
                '","fan":"' + fan_mode + hold_time +
                '","isTemperatureAbsolute":false,"isTemperatureRelative":false}}],'
                '"selection":{"selectionType":"thermostats","selectionMatch"'
                ':"' + self.thermostats[index]['identifier'] + '"}}')
        request = requests.post(url, headers=header, params=params, data=body)
        if request.status_code == requests.codes.ok:
            return request
        else:
            LOGGER.warn("Error connecting to Ecobee while attempting to set"
                  " a hold and fan off.  Refreshing tokens...")
            self.refresh_tokens()

    def turn_fan_off(self, index, cool_temp=82, heat_temp=69,
                      hold_type="indefinite", duration_minute=0):
        ''' Set a fan off '''

        # Get the current hvac mode and use it later to set the thermostat back if needed
        current_hvac_mode = self.get_hvac_mode(index)

        request = self.set_hvac_mode(index, HVAC_MODE_OFF)
        if request.status_code == requests.codes.ok:
            request = self._turn_fan_off(index, cool_temp, heat_temp, hold_type, duration_minute) 

            if request.status_code == requests.codes.ok:
                # set the thermostat back when needed - For home deployment.
                # Important to put the thermostat to the original state
                #if current_hvac_mode != HVAC_MODE_OFF:
                #    request = self.set_hvac_mode(index, current_hvac_mode)

                return request
            else:
                LOGGER.warn("Error connecting to Ecobee while attempting to set"
                      " fan mode.  Refreshing tokens...")
                self.refresh_tokens()
        else:
            LOGGER.warn("Error connecting to Ecobee while attempting to set"
                    " fan off.  Refreshing tokens...")
            self.refresh_tokens()

    def get_occupancy(self, index):
        ''' Get occupancy '''

        thermostat = self.thermostats[index]
        isOccupied = False
        if thermostat is not None:
            for sensor in thermostat['remoteSensors']:
                for capability in sensor['capability']:
                    if capability['type'] == 'occupancy':
                        isOccupied = capability['value'] in ['true', '1', 'yes']
                        if isOccupied == True:
                            break

            #isOccupied = any(sensor['capability'][2]['value'] for sensor in thermostat['remoteSensors'])
        else:
            raise Exception("Thermostat doesn't exist for the index: {}".format(index))

        return isOccupied

    def get_hvac_mode(self, index):
        ''' Get hvac mode '''

        thermostat = self.thermostats[index]
        if thermostat is not None:
            return thermostat['settings']['hvacMode']

    def get_hold_action(self, index):
        ''' Get hold action '''

        thermostat = self.thermostats[index]
        if thermostat is not None:
            return thermostat['settings']['holdAction']

    def get_desired_fanmode(self, index):
        ''' Get desired fanmode '''

        thermostat = self.thermostats[index]
        if thermostat is not None:
            return thermostat['runtime']['desiredFanMode']

    def get_desired_heat(self, index):
        ''' Get desired heat temperature '''

        thermostat = self.thermostats[index]
        if thermostat is not None:
            return thermostat['runtime']['desiredHeat']

    def get_desired_cool_heat(self, index):
        ''' Get desired heat temperature '''

        thermostat = self.thermostats[index]
        if thermostat is not None:
            current_climate_ref = thermostat['program']['currentClimateRef']
            climate_ref = next(filter(lambda climate: climate['climateRef'] == current_climate_ref, thermostat['program']['climates']))

            return climate_ref['coolTemp'], climate_ref['heatTemp']

    def get_desired_cool(self, index):
        ''' Get desired heat temperature '''

        thermostat = self.thermostats[index]
        if thermostat is not None:
            return thermostat['runtime']['desiredCool']

    def get_thermostat_data(self, index, fieldname):
        ''' Get thermostat state value '''
        thermostat = self.thermostats[index]
        if thermostat is not None:
            return thermostat[fieldname]

    def get_settings_data(self, index, fieldname):
        ''' Get field value '''

        thermostat = self.thermostats[index]
        if thermostat is not None:
            return thermostat['settings'][fieldname]


    def get_runtime_data(self, index, fieldname):
        ''' Get desired runtime field value '''

        thermostat = self.thermostats[index]
        if thermostat is not None:
            return thermostat['runtime'][fieldname]