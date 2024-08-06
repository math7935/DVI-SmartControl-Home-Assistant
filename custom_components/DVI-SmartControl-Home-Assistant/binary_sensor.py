from homeassistant.components.binary_sensor import BinarySensorEntity
from .const import DOMAIN

def setup_platform(hass, config, add_entities, discovery_info=None):
    username = config[CONF_USERNAME]
    password = config[CONF_PASSWORD]
    fab_no = config[CONF_FAB_NO]
    scan_interval = config[CONF_SCAN_INTERVAL]

    binary_sensors = [
        DviHeatpumpBinarySensor("DVI Heatpump Hotwater on", username, password, fab_no, scan_interval),
        # Add other binary sensor entities similarly
    ]

    add_entities(binary_sensors, True)

class DviHeatpumpBinarySensor(BinarySensorEntity):
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
    def is_on(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        # Perform REST API call to update the sensor state and attributes
        response = self.get_heatpump_data()
        if response:
            self._state = response.get('output', {}).get('userSettings', {}).get('Hotwater.State', False)
            self._attributes = response.get('output', {}).get('userSettings', {})

    def get_heatpump_data(self):
        import requests
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
            self._state = False
            self._attributes = {"error": str(e)}
            return None
