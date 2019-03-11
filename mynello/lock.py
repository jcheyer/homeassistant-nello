#
# For more details, please refer to github at
# https://github.com/jcheyer/homeassistant-nello
#
"""
Nello.io lock platform.
For more details about this platform, please refer to the documentation
https://home-assistant.io/components/lock.nello/
"""
from itertools import filterfalse
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.lock import (LockDevice, PLATFORM_SCHEMA)
from homeassistant.const import (CONF_PASSWORD, CONF_USERNAME)

REQUIREMENTS = ['pynello==2.0.2']

_LOGGER = logging.getLogger(__name__)

ATTR_ADDRESS = 'address'
ATTR_LOCATION_ID = 'location_id'
EVENT_DOOR_BELL = 'nello_bell_ring'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Nello lock platform."""
    from pynello.private import Nello
    nello = Nello(config.get(CONF_USERNAME), config.get(CONF_PASSWORD))
    add_entities([NelloLock(lock) for lock in nello.locations], True)


class NelloLock(LockDevice):
    """Representation of a Nello lock."""

    def __init__(self, nello_lock):
        """Initialize the lock."""
        self._nello_lock = nello_lock
        self._device_attrs = None
        self._activity = None
        self._name = None
        self._nello_lock.update()
        # Location identifiers
        location_id = self._nello_lock.location_id
        short_id = self._nello_lock.short_id
        address = self._nello_lock.address
        self._name = 'Nello {}'.format(short_id)
        self._device_attrs = {
            ATTR_ADDRESS: address,
            ATTR_LOCATION_ID: location_id
        }

    @property
    def name(self):
        """Return the name of the lock."""
        return self._name

    @property
    def is_locked(self):
        """Return true if lock is locked."""
        return True

    @property
    def device_state_attributes(self):
        """Return the device specific state attributes."""
        return self._device_attrs

    def update(self):
        """Update the nello lock properties."""

    def unlock(self, **kwargs):
        """Unlock the device."""
        if not self._nello_lock.open_door():
            _LOGGER.error("Failed to unlock")