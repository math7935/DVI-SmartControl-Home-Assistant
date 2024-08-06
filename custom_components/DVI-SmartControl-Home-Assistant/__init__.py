DOMAIN = "dvi_heatpump"

async def async_setup(hass, config):
    """Set up the DVI Heatpump component."""
    return True

async def async_setup_entry(hass, entry):
    """Set up DVI Heatpump from a config entry."""
    hass.data[DOMAIN] = entry.data
    # Initialize your rest sensors here
    return True

async def async_unload_entry(hass, entry):
    """Unload DVI Heatpump config entry."""
    hass.data.pop(DOMAIN)
    return True
