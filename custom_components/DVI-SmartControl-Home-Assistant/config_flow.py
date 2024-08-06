import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD, CONF_FAB_NO, CONF_SCAN_INTERVAL, CONF_HEATPUMP_TYPE

class DviHeatpumpConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return DviHeatpumpOptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="DVI Heatpump", data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
            vol.Required(CONF_FAB_NO): str,
            vol.Optional(CONF_SCAN_INTERVAL, default=5): int,
            vol.Required(CONF_HEATPUMP_TYPE): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)

class DviHeatpumpOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Optional(CONF_SCAN_INTERVAL, default=self.config_entry.options.get(CONF_SCAN_INTERVAL, 5)): int,
        })

        return self.async_show_form(step_id="init", data_schema=options_schema)
