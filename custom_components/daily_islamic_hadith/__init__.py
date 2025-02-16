from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, FETCH_HADITH_SERVICE

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the custom integration from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Forward the config entry to the sensor platform
    await hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    )

    # Service calling function
    async def handle_fetch_hadith_service(call):
        """Handle the fetch hadith service."""
        sensor = hass.data[DOMAIN]["sensor.daily_hadith"]
        if sensor:
            await sensor.handle_service_call()
        else:
            raise HomeAssistantError("Sensor not found.")

    # register the service
    hass.services.async_register(
        DOMAIN,
        FETCH_HADITH_SERVICE,
        handle_fetch_hadith_service
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
