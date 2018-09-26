# Install TESS (Thing-Enabled Self-Science) for SmartAir

## Prerequisites
- Set up a PRISMS gateway ([here](https://github.com/VDL-PRISM/docs/blob/master/gateway_setup.md))
- Set up UMDS Dylos sensors ([here](https://github.com/VDL-PRISM/docs/blob/master/dylos_setup.md))
- Set up a PRISMS server ([here](https://github.com/VDL-PRISM/docs/blob/master/server_setup.md))
- Install Ansible Playbook on a personal (deployment) computer

## 1. Download TESS
Download TESS code to an empty directory on an personal (installation) computer.
You can use git command or use a git client program to download the TESS source code. 
The git command is shown below.

```bash
git clone https://github.com/VDL-PRISM/TESS.git
```

## 2. Customize TESS for SmartAir
After the TESS source code is downloaded to a local directory, For SmartAir, edit the configuration file by following the following instructions.

## 2.1 Update configuration file
- Open the configuration.yaml file under /tess/rules/thermostats/ecobee in Edit mode
- Change [CHANGE ME] parts in the configuration yaml for your deployment setting. For example, in the actuator_handler section, the [CHANGE ME] for home_id is "prisms-gateway". This home id is the same home id when a PRISMS gateway is set up.


### 2.1.1 Update [CHANGE ME] in actuator_handler
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

### 2.1.2 Update sensors
(e.g., sensor1: monitor12, sensor2: monitor13, sensor3: monitor14)

```bash
sensors: &sensorlist
  - sensor1: [CHANGE ME]
  - sensor2: [CHANGE ME]
  - sensor3: [CHANGE ME]
```

### 2.1.3 Update tess_database
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


## 3. Set up Ecobee Thermostat Actuator for SmartAir

[Instructions for setting up Ecobee Thermostat Actuator](ecobee_setup.md)



## 4. Update Ansible deployment script for SmartAir 
The TESS-ansible is the central TESS deployment script and is a part of TESS source code. 
The deployment script can be customized for various applications by updating the playbook.yaml.

### 4.1 Change ecobee_controller.conf under templates directory
You can find the Ecobee controller application API key from My Apps after logging in Ecobee Website ([here](https://www.ecobee.com))

```bash
{"API_KEY": "{{ controller_api_key }}"}
```

### 4.2 Change ecobee_monitor.conf under templates directory
You can find the Ecobee monitor application API key from My Apps in Ecobee Website ([here](https://www.ecobee.com))

```bash
{"API_KEY": "{{ monitor_api_key }}"}
```

### 4.3 Update inventory.ini 
Update the ip for the target PRISMS gateway server 

```bash
[servers]
10.0.0.9
```

### 4.4 Run Ansible playbook script to deploy TESS and SmartAir to the PRISMS gateway
- Start a new terminal session on TESS-ansible directory. 
- Enter the following command to the command terminal

```bash
ansible-playbook playbook.yaml -i inventory.ini
```
[Example output of successful deployment using TESS ansible-playbook](ansible_deployment.md)


## 5. Finished

