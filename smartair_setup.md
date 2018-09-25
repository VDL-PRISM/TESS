# Set up SmartAir

## Prerequisites
- Install TESS ([here](https://github.com/VDL-PRISM/TESS/blob/master/tess_setup.md))


## Update configuration file
- Open the configuration.yaml file under /tess/rules/thermostats/ecobee in Edit mode
- Change [CHANGE ME] parts in the configuration yaml for your deployment setting. For example, in the actuator_handler section, the [CHANGE ME] for home_id is "prisms-gateway". This home id is the same home id when a PRISMS gateway is set up.


### Update [CHANGE ME] in actuator_handler
(e.g., home_id: prisms-gateway)

```bash
actuator_handler:
  modulename: 'tess.actuators.thermostats.ecobee_actuator'
  classname: 'EcobeeActuator'
  controller_config_file: 'ecobee_controller.conf'
  monitor_config_file: 'ecobee_monitor.conf'
  actuator_id: 0
  home_id: [CHANGE ME]
  actuator_min_on_minutes_per_hour: [20, 40]
```

### Update sensors
(e.g., sensor1: monitor12, sensor2: monitor13, sensor3: monitor14)

```bash
sensors: &sensorlist
  - sensor1: [CHANGE ME]
  - sensor2: [CHANGE ME]
  - sensor3: [CHANGE ME]
```

### Update tess_database
(e.g., host: prisms.app.lundrigan.org, port: 443, database: home_assistant, ssl: True)

```bash
tess_database:
  username: [CHANGE ME]
  password: [CHANGE ME]
  host: [CHANGE ME]
  port: [CHANGE ME]
  database: [CHANGE ME]
  ssl: [CHANGE ME]
```



## TESS Controller Service

```bash
[Unit]
Description=TESS Controller 
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/srv/pi/TESS
ExecStartPre=source /srv/pi/TESS/bin/activate
ExecStart=/srv/pi/TESS/bin/python main.py controller actuator_controller.conf tess/rules/thermostat/ecobee/configuration.yaml tess/automations/logging_controller.yaml > tess-controller.log 2>&1

[Install]
WantedBy=multi-user.target
```

## TESS Monitor Service

```bash
[Unit]
Description=TESS Monitor 
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/srv/pi/TESS
ExecStartPre=source /srv/pi/TESS/bin/activate
ExecStart=/srv/pi/TESS/bin/python main.py actuator_monitor.conf tess/rules/thermostat/ecobee/configuration.yaml tess/automations/logging_monitor.yaml > tess-monitor.log 2>&1

[Install]
WantedBy=multi-user.target
```
