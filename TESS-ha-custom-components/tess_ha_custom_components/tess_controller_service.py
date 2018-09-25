import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'tess_controller_service'

ATTR_NAME = 'name'
DEFAULT_NAME = 'TESS Ecobee Controller'

def setup(hass, config):
    """Setup is called when Home Assistant is loading our component."""
    _LOGGER.info("Setup the TESS Controller")

    def handle_start(call):
        name = call.data.get(ATTR_NAME, DEFAULT_NAME)

        hass.states.set('tess_controller_service.start', name)
    
    hass.services.register(DOMAIN, 'tess_controller', handle_start)

    # Return boolean to indicate that initialization was successfully.
    return True
