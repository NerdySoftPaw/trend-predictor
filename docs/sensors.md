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

Shows how many hours it will take at the current trend to reach the target value.

- Unit: `h` (hours, as decimal — e.g. `4.2`)
- To display minutes in a dashboard: `{{ (states('sensor.xyz_time_remaining') | float * 60) | round }} min`
- Shows `unavailable` when:
    - Fewer than 2 data points in the time window
    - The trend is moving away from the target value
    - The source sensor does not provide a numeric value

## Rate of change

The current rate of change of the source sensor per hour, calculated via linear regression.

- Unit: dynamic — `%/h` if the source sensor uses `%`, otherwise `<unit>/h`
- Negative = value is falling, Positive = value is rising
- Useful for diagnostics: e.g. `-3.5 %/h` means the battery is losing 3.5% per hour

## Predicted time

The concrete point in time at which the target value is expected to be reached — as a timestamp sensor.

- Device class: `timestamp` → HA formats it automatically as date/time
- Can be used directly as a time trigger in automations
- Shows `unavailable` under the same conditions as the time remaining sensor

---

## How the calculation works

The integration collects all state changes of the source sensor within the configured time window and calculates a trend line using **linear regression** (least squares). The time remaining until the target value is derived from the current value and the slope of this line.

```
Time remaining (h) = (target value − current value) / rate of change
```

Linear regression over multiple points is more robust than a simple first/last difference because short-term outliers carry less weight.
