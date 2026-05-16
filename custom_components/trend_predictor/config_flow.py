import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry

from .const import (
    CONF_MAX_VALUE,
    CONF_MIN_VALUE,
    CONF_SOURCE_ENTITY,
    CONF_TIME_WINDOW,
    DEFAULT_MAX_VALUE,
    DEFAULT_MIN_VALUE,
    DEFAULT_TIME_WINDOW,
    DOMAIN,
)


def _build_schema(defaults: dict) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(
                CONF_SOURCE_ENTITY,
                default=defaults.get(CONF_SOURCE_ENTITY),
            ): selector.EntitySelector(selector.EntitySelectorConfig(domain=["sensor", "input_number"])),
            vol.Required(
                CONF_MIN_VALUE,
                default=defaults.get(CONF_MIN_VALUE, DEFAULT_MIN_VALUE),
            ): selector.NumberSelector(selector.NumberSelectorConfig(mode="box", step=0.1)),
            vol.Required(
                CONF_MAX_VALUE,
                default=defaults.get(CONF_MAX_VALUE, DEFAULT_MAX_VALUE),
            ): selector.NumberSelector(selector.NumberSelectorConfig(mode="box", step=0.1)),
            vol.Required(
                CONF_TIME_WINDOW,
                default=defaults.get(CONF_TIME_WINDOW, DEFAULT_TIME_WINDOW),
            ): selector.NumberSelector(
                selector.NumberSelectorConfig(min=5, max=1440, step=5, unit_of_measurement="min", mode="slider")
            ),
        }
    )


class TrendPredictorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            entity_id = user_input[CONF_SOURCE_ENTITY]
            await self.async_set_unique_id(entity_id)
            self._abort_if_unique_id_configured()

            er = async_get_entity_registry(self.hass)
            entry = er.async_get(entity_id)
            name = entry.name or entry.original_name if entry else entity_id
            min_v = user_input[CONF_MIN_VALUE]
            max_v = user_input[CONF_MAX_VALUE]

            return self.async_create_entry(
                title=f"{name} ({min_v}–{max_v})",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_build_schema({}),
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return TrendPredictorOptionsFlow(config_entry)


class TrendPredictorOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=_build_schema({**self._config_entry.data, **self._config_entry.options}),
        )
