import requests
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD, CONF_FAB_NO, CONF_SCAN_INTERVAL

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_FAB_NO): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=5): cv.positive_int,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]
    fab_no = config[CONF_FAB_NO]
    scan_interval = config[CONF_SCAN_INTERVAL]

    sensors = [
        DviHeatpumpSensor("DVI Heatpump Sensors", username, password, fab_no, scan_interval),
        # Add other sensor entities similarly
    ]

    add_entities(sensors, True)

class DviHeatpumpSensor(SensorEntity):
    def __init__(self, name, username, password, fab_no, scan_interval):
        self._name = name
        self._username = username
        self._password = password
        self._fab_no = fab_no
        self._scan_interval = scan_interval
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        # Perform REST API call to update the sensor state and attributes
        response = self.get_heatpump_data()
        if response:
            self._state = "OK"
            self._attributes = response.get('output', {}).get('sensor', {})

    def get_heatpump_data(self):
        payload = {
            "usermail": self._username,
            "userpassword": self._password,
            "fabnr": self._fab_no,
            "get": {
                "bestgreen": 0,
                "sensor": 1,
                "relay": 1,
                "timer": 0,
                "userSettings": 1
            }
        }
        try:
            response = requests.post("https://ws.dvienergi.com/API/", json=payload)
            return response.json()
        except requests.exceptions.RequestException as e:
            self._state = "Error"
            self._attributes = {"error": str(e)}
            return None
