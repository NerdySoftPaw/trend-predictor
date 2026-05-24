import logging
from collections import deque
from datetime import timedelta

from homeassistant.components.persistent_notification import async_create as async_create_notification
from homeassistant.components.recorder import get_instance
from homeassistant.components.recorder.history import get_significant_states
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_call_later, async_track_state_change_event
from homeassistant.util import dt as dt_util

from .const import CONF_MAX_VALUE, CONF_MIN_VALUE, CONF_SOURCE_ENTITY, CONF_TIME_WINDOW, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    config = {**entry.data, **entry.options}
    source_entity = config[CONF_SOURCE_ENTITY]
    min_value = float(config[CONF_MIN_VALUE])
    max_value = float(config[CONF_MAX_VALUE])
    time_window = int(config[CONF_TIME_WINDOW])

    if min_value >= max_value:
        _LOGGER.warning(
            "min_value (%s) must be less than max_value (%s); swapping values",
            min_value,
            max_value,
        )
        min_value, max_value = max_value, min_value
        async_create_notification(
            hass,
            title="Trend Predictor: Configuration corrected",
            message=(
                f"**{entry.title}**: Minimum value was greater than or equal to maximum value. "
                f"The values have been swapped automatically. "
                f"Please reconfigure this entry to fix it permanently."
            ),
            notification_id=f"{DOMAIN}_min_max_swap_{entry.entry_id}",
        )

    data = TrendPredictorData(hass, source_entity, min_value, max_value, time_window)

    sensors = [
        TrendPredictorTimeRemainingSensor(data, entry),
        TrendPredictorRateSensor(data, entry),
        TrendPredictorTimestampSensor(data, entry),
    ]

    async_add_entities(sensors)
    await data.async_start()


class TrendPredictorData:
    """Shared data and history management for one config entry."""

    def __init__(self, hass, source_entity, min_value, max_value, time_window_minutes):
        self.hass = hass
        self.source_entity = source_entity
        self.min_value = min_value
        self.max_value = max_value
        self.time_window = time_window_minutes
        self._history: deque[tuple] = deque()
        self._listeners: list = []
        self._unsubscribe = None
        self._debounce_unsub = None

        self.rate = None
        self.hours_remaining = None
        self.predicted_time = None
        self.active_target = None

    def register_listener(self, sensor):
        self._listeners.append(sensor)

    async def async_start(self):
        end = dt_util.utcnow()
        start = end - timedelta(minutes=self.time_window)
        try:
            states = await get_instance(self.hass).async_add_executor_job(
                get_significant_states,
                self.hass,
                start,
                end,
                [self.source_entity],
            )
            for state in states.get(self.source_entity, []):
                try:
                    self._history.append((state.last_updated, float(state.state)))
                except (ValueError, TypeError):
                    pass
        except Exception as err:
            _LOGGER.debug("Could not pre-load history from recorder: %s", err)

        self._unsubscribe = async_track_state_change_event(self.hass, [self.source_entity], self._on_state_change)
        self._recalculate()

    def async_stop(self):
        if self._unsubscribe:
            self._unsubscribe()
        if self._debounce_unsub:
            self._debounce_unsub()

    @callback
    def _on_state_change(self, event):
        new_state = event.data.get("new_state")
        if new_state is None:
            return
        try:
            value = float(new_state.state)
        except (ValueError, TypeError):
            return

        now = dt_util.utcnow()
        self._history.append((now, value))

        cutoff = now - timedelta(minutes=self.time_window)
        while self._history and self._history[0][0] < cutoff:
            self._history.popleft()

        if self._debounce_unsub is not None:
            self._debounce_unsub()
        self._debounce_unsub = async_call_later(self.hass, 1, self._debounced_recalculate)

    @callback
    def _debounced_recalculate(self, _now):
        self._debounce_unsub = None
        self._recalculate()
        for sensor in self._listeners:
            sensor.async_write_ha_state()

    def _recalculate(self):
        history = list(self._history)
        if len(history) < 2:
            self.rate = None
            self.hours_remaining = None
            self.predicted_time = None
            self.active_target = None
            return

        t0 = history[0][0]
        times = [(t - t0).total_seconds() / 3600 for t, _ in history]
        values = [v for _, v in history]

        n = len(times)
        sum_t = sum(times)
        sum_v = sum(values)
        sum_tv = sum(t * v for t, v in zip(times, values))
        sum_t2 = sum(t * t for t in times)

        denom = n * sum_t2 - sum_t**2
        if denom == 0:
            self.rate = None
            self.hours_remaining = None
            self.predicted_time = None
            self.active_target = None
            return

        rate = (n * sum_tv - sum_t * sum_v) / denom
        intercept = (sum_v - rate * sum_t) / n
        current_v = rate * times[-1] + intercept
        self.rate = round(rate, 4)

        if rate == 0:
            self.hours_remaining = None
            self.predicted_time = None
            self.active_target = None
            return

        # Auto-select target based on trend direction
        target = self.min_value if rate < 0 else self.max_value
        self.active_target = target

        hours = (target - current_v) / rate

        if hours < 0:
            self.hours_remaining = None
            self.predicted_time = None
        else:
            self.hours_remaining = round(hours, 2)
            self.predicted_time = dt_util.utcnow() + timedelta(hours=hours)


class _TrendPredictorBaseSensor(SensorEntity):
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, data: TrendPredictorData, entry: ConfigEntry, key: str):
        self._data = data
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="Trend Predictor",
        )
        data.register_listener(self)

    async def async_added_to_hass(self):
        pass

    async def async_will_remove_from_hass(self):
        self._data._listeners = [s for s in self._data._listeners if s is not self]
        if not self._data._listeners:
            self._data.async_stop()

    @property
    def available(self) -> bool:
        return True


class TrendPredictorTimeRemainingSensor(_TrendPredictorBaseSensor):
    _attr_icon = "mdi:timer-outline"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "h"

    def __init__(self, data, entry):
        super().__init__(data, entry, "time_remaining")
        self._attr_translation_key = "time_remaining"

    @property
    def native_value(self):
        return self._data.hours_remaining

    @property
    def extra_state_attributes(self):
        return {"target": self._data.active_target}


class TrendPredictorRateSensor(_TrendPredictorBaseSensor):
    _attr_icon = "mdi:chart-line"
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, data, entry):
        super().__init__(data, entry, "rate")
        self._attr_translation_key = "rate"

    @property
    def native_value(self):
        return self._data.rate

    @property
    def native_unit_of_measurement(self):
        state = self.hass.states.get(self._data.source_entity)
        if state:
            unit = state.attributes.get("unit_of_measurement", "")
            return f"{unit}/h" if unit else "/h"
        return "/h"


class TrendPredictorTimestampSensor(_TrendPredictorBaseSensor):
    _attr_icon = "mdi:clock-end"
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, data, entry):
        super().__init__(data, entry, "predicted_time")
        self._attr_translation_key = "predicted_time"

    @property
    def native_value(self):
        return self._data.predicted_time

    @property
    def extra_state_attributes(self):
        return {"target": self._data.active_target}
