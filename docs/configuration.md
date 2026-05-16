# Configuration

All configuration is done through the Home Assistant UI — no YAML required.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| **Source entity** | Entity ID | — | Numeric sensor whose history is analysed |
| **Target value** | Number | `0` | Value the prediction is calculated towards |
| **Time window** | Minutes | `30` | How much history is used for the calculation |

## Source entity

Entities of type `sensor` and `input_number` are supported. The current state must be a numeric value (not `unknown` or `unavailable`).

## Target value

- "When will the battery be empty?" → `0`
- "When will the battery be full?" → `100`
- Any other value works too (e.g. minimum fill level, critical temperature)

## Time window

The time window determines how many minutes of history are included in the linear regression.

- **Short window (5–15 min):** Reacts quickly to changes in consumption but more sensitive to short-term fluctuations
- **Medium window (30 min):** Good balance for most use cases
- **Long window (60–120 min):** Stable estimate for steady trends, slower to react to changes

!!! tip
    On startup the integration automatically loads the last `n` minutes from the HA database (Recorder). Sensors are active immediately after a restart.

## Reconfiguring

All parameters can be changed at any time via **Settings → Devices & Services → Trend Predictor → Configure**.
