# TESS Security and Safety

The TESS developers and end users should follow common security practices.
(e.g., Do not store passwords in a plain text. Use a strong password.) 

The following are some important security and sefety measures that the users of TESS should be aware before using TESS.

## Do not check in API Keys
TESS connects sensors and IoT actuators that sometimes require interactions with cloud APIs with API keys. 
These API keys SHOULD NOT be checked into the Github public repo for security concerns and safety of people.

## Do not check in private and personal information
It is easy to forget to remove some of sensitive information while developing and testing modules and configuration files. 

## Actuators can be dangerous.
TESS allows connecting actuators that may control phyical objects in home. Before you connect actuators to TESS, you should know what you are doing and always be cautious.

