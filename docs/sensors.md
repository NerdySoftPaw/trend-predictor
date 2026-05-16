# Sensors

One integration instance creates three sensors, all grouped under a single device.

## Overview

| Sensor | Unit | Device Class | State Class |
|--------|------|--------------|-------------|
| Time remaining | `h` | — | Measurement |
| Rate of change | `<unit>/h` | — | Measurement |
| Predicted time | — | `timestamp` | — |

---

## Time remaining

Shows how many hours it will take at the current trend to reach the active target (minimum or maximum, depending on direction).

- Unit: `h` (hours, as decimal — e.g. `4.2`)
- To display minutes in a dashboard: `{{ (states('sensor.xyz_time_remaining') | float * 60) | round }} min`
- Shows `unavailable` when:
    - Fewer than 2 data points in the time window
    - The source sensor does not provide a numeric value
    - The rate is exactly zero (flat trend)
- **Attribute `target`:** which value is currently being predicted towards (min or max)

## Rate of change

The current rate of change of the source sensor per hour, calculated via linear regression.

- Unit: dynamic — `%/h` if the source sensor uses `%`, otherwise `<unit>/h`
- Negative = value is falling → integration predicts time to **minimum**
- Positive = value is rising → integration predicts time to **maximum**

## Predicted time

The concrete point in time at which the active target is expected to be reached — as a timestamp sensor.

- Device class: `timestamp` → HA formats it automatically as date/time
- Can be used directly as a time trigger in automations
- Shows `unavailable` under the same conditions as the time remaining sensor
- **Attribute `target`:** which value is currently being predicted towards

---

## How direction detection works

The integration picks the target automatically based on the regression slope:

```
rate < 0  →  target = min_value  (e.g. 0)
rate > 0  →  target = max_value  (e.g. 100)

time remaining = (target − current value) / rate
```

When a PV battery switches from discharging to charging, the rate sign flips and both the target and the predicted time update automatically — no reconfiguration needed.

---

## How the calculation works

The integration collects all state changes of the source sensor within the configured time window and calculates a trend line using **linear regression** (least squares). The time remaining is derived from the current value, the slope, and the active target.

Linear regression over multiple points is more robust than a simple first/last difference because short-term outliers carry less weight.
