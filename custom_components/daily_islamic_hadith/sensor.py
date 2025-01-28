import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util.dt import as_local

from .const import DOMAIN, LANG_AR

_LOGGER = logging.getLogger(__name__)


class DailyHadithUpdateCoordinator:

    def __init__(self, hass, http_client, hadith_lang):
        """Initialize the coordinator."""
        self.hass = hass
        self.http_client = http_client
        self.api = "https://dailyislamichadith.com/api/fetch-hadith?fetch-mode=DAILY&lang=" + hadith_lang
        self.data = {}
        self.last_update = None
        if hadith_lang == LANG_AR:
            self.hadith_key = "hadithArabic"
            self.hadith_explanation_key = "hadithExplanationArabic"
        else:
            self.hadith_key = "hadithEnglish"
            self.hadith_explanation_key = "hadithExplanationEnglish"

    async def async_update_data(self):
        """Fetch data from the API."""
        _LOGGER.info("Fetching new hadith from API...")
        try:
            async with self.http_client.get(self.api) as response:
                if response.status == 200:
                    json_response = await response.json()
                    self.data = {
                        "hadith": json_response.get(self.hadith_key),
                        "hadith_explanation": json_response.get(self.hadith_explanation_key),
                    }
                    self.last_update = as_local(datetime.now())
                    _LOGGER.info("Successfully updated daily hadith: %s", self.data)
                else:
                    _LOGGER.error("Error fetching hadith from API: %s", response.status)
        except Exception as e:
            _LOGGER.error("Error fetching hadith: %s", e)

    async def async_config_entry_first_refresh(self):
        await self.async_update_data()


class HadithAPISensor(SensorEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = "Daily Hadith"
        self._attr_unique_id = "daily_hadith"
        self._state = "Fetching"
        self._attributes = {}

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the additional attributes of the sensor."""
        return self._attributes

    async def async_update(self):
        """Update the sensor state."""
        await self.coordinator.async_update_data()
        # Update attributes with API data
        self._attributes = {
            "hadith": self.coordinator.data.get("hadith"),
            "explanation": self.coordinator.data.get("hadith_explanation"),
            "last_update": self.coordinator.last_update.isoformat() if self.coordinator.last_update else None,
        }
        self._state = "Updated"

    async def async_added_to_hass(self):
        """Set up periodic updates."""
        self.async_on_remove(
            async_track_time_change(
                self.coordinator.hass,
                self.update_callback,
                hour=1, minute=0, second=0
            )
        )

    async def update_callback(self, now):
        """Fetch new data and update state."""
        await self.async_update()
        self.async_write_ha_state()


async def async_setup_entry(hass, config_entry, async_add_entities):
    async def config_update_listener(hass, config_entry):
        await hass.config_entries.async_reload(config_entry.entry_id)

    config_entry.async_on_unload(
        config_entry.add_update_listener(config_update_listener)
    )
    http_client = async_get_clientsession(hass)
    """Set up the single sensor from a config entry."""
    hadith_lang = config_entry.options.get("Hadith Language", config_entry.data["Hadith Language"])

    coordinator = DailyHadithUpdateCoordinator(hass, http_client, hadith_lang)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([HadithAPISensor(coordinator)])
