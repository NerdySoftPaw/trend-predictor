# Configuration

All configuration is done through the Home Assistant UI — no YAML required.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| **Source entity** | Entity ID | — | Numeric sensor whose history is analysed |
| **Minimum value** | Number | `0` | Lower bound — predicted when the trend is falling |
| **Maximum value** | Number | `100` | Upper bound — predicted when the trend is rising |
| **Time window** | Minutes | `30` | How much history is used for the calculation |

!!! warning
    Minimum value must be **less than** maximum value. The UI will show an error if you enter them the wrong way around. Existing entries with swapped values are automatically corrected on the next HA restart.

## Source entity

Entities of type `sensor` and `input_number` are supported. The current state must be a numeric value (not `unknown` or `unavailable`).

## Automatic direction detection

The integration detects the trend direction automatically and picks the right target:

- **Trend is falling** (rate < 0) → predicts time until **minimum value**
- **Trend is rising** (rate > 0) → predicts time until **maximum value**

No manual switching needed. If a PV battery is discharging, the sensors predict when it will reach 0%. Once it starts charging, they automatically switch to predicting when it will reach 100%.

The currently active target is exposed as a `target` attribute on the time remaining and predicted time sensors.

## Time window

The time window determines how many minutes of history are included in the linear regression.

- **Short window (5–15 min):** Reacts quickly to changes in consumption but more sensitive to short-term fluctuations
- **Medium window (30 min):** Good balance for most use cases
- **Long window (60–120 min):** Stable estimate for steady trends, slower to react to changes

!!! tip
    On startup the integration automatically loads the last `n` minutes from the HA database (Recorder). Sensors are active immediately after a restart.

## Reconfiguring

All parameters can be changed at any time via **Settings → Devices & Services → Trend Predictor → Configure**.
