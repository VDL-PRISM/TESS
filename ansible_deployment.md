## TESS Ansible Script Deployment

204-99-170-217:TESS-ansible kyeongmin$ ansible-playbook playbook.yaml -i inventory.ini 

PLAY [Set up TESS Ecobee Controller and Monitor] *******************************

TASK [setup] *******************************************************************
ok: [10.0.0.215]

TASK [Update packages] *********************************************************
ok: [10.0.0.215]

TASK [Install necessary packages] **********************************************
ok: [10.0.0.215] => (item=[u'git', u'python-dev', u'python-setuptools'])

TASK [Install pip] *************************************************************
changed: [10.0.0.215]

TASK [Install virtualenv python package] ***************************************
ok: [10.0.0.215]

TASK [Check for the virtualenv folder] *****************************************
ok: [10.0.0.215]

TASK [Create the srv/pi directory] *********************************************
skipping: [10.0.0.215]

TASK [Create a virtualenv for TESS] ********************************************
skipping: [10.0.0.215]

TASK [Change owner of the folder] **********************************************
skipping: [10.0.0.215]

TASK [Install TESS Ecobee Controller code] *************************************
ok: [10.0.0.215]

TASK [Check for ecobee_controller.conf file for TESS Ecobee Controller] ********
ok: [10.0.0.215]

TASK [Set up ecobee_controller.conf file for TESS Ecobee Controller] ***********
skipping: [10.0.0.215]

TASK [Check for ecobee_monitor.conf file for TESS Ecobee Monitor] **************
ok: [10.0.0.215]

TASK [Set up ecobee_monitor.conf file for TESS Ecobee Monitor] *****************
skipping: [10.0.0.215]

TASK [Activate the virtualenv and install requirements] ************************
changed: [10.0.0.215]

TASK [Set up TESS controller service to run on boot] ***************************
ok: [10.0.0.215]

TASK [Restart the TESS Ecobee Controller service] ******************************
skipping: [10.0.0.215]

TASK [Set up monitor service to run on boot] ***********************************
ok: [10.0.0.215]

TASK [Restart the TESS Ecobee Monitor service] *********************************
skipping: [10.0.0.215]

PLAY RECAP *********************************************************************
10.0.0.215                 : ok=12   changed=2    unreachable=0    failed=0   
