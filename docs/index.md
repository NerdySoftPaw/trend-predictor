# Trend Predictor

Trend Predictor is a Home Assistant integration that predicts when any numeric sensor will reach a target value — based on its current trend.

## How it works

The integration watches a sensor (e.g. battery state of charge in percent), analyses its history over a configurable time window and uses linear regression to calculate when the sensor will reach a defined target. The direction is detected automatically: if the value is falling, it predicts time to the minimum; if it is rising, it predicts time to the maximum.

## The three sensors

| Sensor | Example value | Description |
|--------|--------------|-------------|
| **Time remaining** | `4.2 h` | Hours until the active target is reached |
| **Rate of change** | `-3.5 %/h` | Current rate of change per hour |
| **Predicted time** | `2026-05-16 20:30` | Concrete timestamp when the target will be reached |

All three sensors show `unavailable` when there are not enough data points or the trend is flat. The currently active target (min or max) is available as an attribute on the time remaining and predicted time sensors.

## Typical use cases

- **PV battery empty:** When will the battery reach 0% at current consumption?
- **PV battery full:** When will the battery reach 100% at current charge rate?
- **Cistern:** When will the water tank run dry at current usage?
- **Heating oil tank:** Order in advance before the tank runs out
- **Temperature sensor:** When will the basement cool to a critical temperature?

## Quick start

!!! tip "Set up in 3 steps"
    1. Install Trend Predictor via HACS
    2. Restart Home Assistant
    3. Settings → Devices & Services → Add Integration → **Trend Predictor**

→ [Installation guide](installation.md)
