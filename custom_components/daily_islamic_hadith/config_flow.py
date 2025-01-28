from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN, LANG_AR, LANG_EN

SUPPORTED_LANGS = [LANG_EN, LANG_AR]

# Define the configuration schema
CONFIG_SCHEMA = vol.Schema({
    vol.Required("Hadith Language"): vol.In(SUPPORTED_LANGS),
})


class CustomIntegrationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            hadith_language = user_input["Hadith Language"]
            if hadith_language not in SUPPORTED_LANGS:
                errors["base"] = "Invalid Language!"
            else:
                # Save configuration
                return self.async_create_entry(title="Daily Islamic Hadith", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
        )

    def async_get_options_flow(self):
        """Return the options flow handler."""
        return CustomIntegrationOptionsFlowHandler()


class CustomIntegrationOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle the options flow for reconfiguration."""

    async def async_step_init(self, user_input=None):
        """Handle the options step."""
        if user_input is not None:
            # Update the options for the integration
            return self.async_create_entry(title="", data=user_input)

        # Fetch the current value or use the default
        current_hadith_lang = self.config_entry.options.get("Hadith Language", self.config_entry.data["Hadith Language"])

        # Show the options form
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("Hadith Language", default=current_hadith_lang): vol.In(SUPPORTED_LANGS),
            }),
        )
