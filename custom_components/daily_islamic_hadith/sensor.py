import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util.dt import as_local

from .const import DOMAIN, LANG_AR, SENSOR_STATE_FETCHING, SENSOR_STATE_UPDATED, RANDOM_FETCH_MODE, DAILY_FETCH_MODE

_LOGGER = logging.getLogger(__name__)


class DailyHadithUpdateCoordinator:

    def __init__(self, hass, http_client, hadith_lang, fetch_mode):
        """Initialize the coordinator."""
        self.hass = hass
        self.http_client = http_client
        self.fetch_mode = fetch_mode
        self.api = None
        self.data = {}
        self.last_update = None
        if hadith_lang == LANG_AR:
            self.hadith_key = "hadithArabic"
            self.hadith_explanation_key = "hadithExplanationArabic"
            self.hadith_lang = hadith_lang
        else:
            self.hadith_key = "hadithEnglish"
            self.hadith_explanation_key = "hadithExplanationEnglish"
            self.hadith_lang = hadith_lang

    async def async_update_data(self):
        """Fetch data from the API."""
        _LOGGER.info("Fetching new hadith from API...")
        self.api = "https://dailyislamichadith.com/api/fetch-hadith?fetch-mode=" + self.fetch_mode + "&lang=" + self.hadith_lang
        try:
            async with self.http_client.get(self.api) as response:
                if response.status == 200:
                    json_response = await response.json()
                    self.data = {
                        "hadith": json_response.get(self.hadith_key),
                        "hadith_explanation": json_response.get(self.hadith_explanation_key),
                        "hadith_language": self.hadith_lang
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
        self._state = SENSOR_STATE_FETCHING
        self._attributes = {}

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return the additional attributes of the sensor."""
        return self._attributes

    @property
    def should_poll(self):
        return False

    def set_state_and_write_to_ha(self, new_state_value):
        self._state = new_state_value
        self.async_write_ha_state()

    async def async_update(self):
        """Update the sensor state."""
        self.set_state_and_write_to_ha(SENSOR_STATE_FETCHING)
        await self.coordinator.async_update_data()
        await self.async_update_sensor_from_current_coordinator_data()

    async def async_update_sensor_from_current_coordinator_data(self):
        # Update sensor attributes from the coordinator data
        self._attributes = {
            "hadith": self.coordinator.data.get("hadith"),
            "explanation": self.coordinator.data.get("hadith_explanation"),
            "language": self.coordinator.data.get("hadith_language"),
            "last_update": self.coordinator.last_update.isoformat() if self.coordinator.last_update else None,
            "last_fetch_mode": self.coordinator.fetch_mode,
        }
        self.set_state_and_write_to_ha(SENSOR_STATE_UPDATED)


    async def async_added_to_hass(self):
        """Set up periodic updates."""
        self.async_on_remove(
            async_track_time_change(
                self.coordinator.hass,
                self.daily_hadith_update,
                hour=1, minute=0, second=0
            )
        )

    async def daily_hadith_update(self, now):
        """Fetch new data and update state."""
        self.coordinator.fetch_mode = DAILY_FETCH_MODE
        await self.async_update()

    async def handle_service_call(self):
        """Fetch new  random data and update state."""
        self.coordinator.fetch_mode = RANDOM_FETCH_MODE
        await self.async_update()


async def async_setup_entry(hass, config_entry, async_add_entities):
    async def config_update_listener(hass, config_entry):
        await hass.config_entries.async_reload(config_entry.entry_id)

    config_entry.async_on_unload(
        config_entry.add_update_listener(config_update_listener)
    )
    http_client = async_get_clientsession(hass)
    """Set up the single sensor from a config entry."""
    hadith_lang = config_entry.options.get("Hadith Language", config_entry.data["Hadith Language"])

    coordinator = DailyHadithUpdateCoordinator(hass, http_client, hadith_lang, DAILY_FETCH_MODE)
    await coordinator.async_config_entry_first_refresh() #first load of hadith into coordinator

    sensor_entity = HadithAPISensor(coordinator)
    async_add_entities([sensor_entity])
    await sensor_entity.async_update_sensor_from_current_coordinator_data()
    hass.data[DOMAIN][sensor_entity.entity_id] = sensor_entity
