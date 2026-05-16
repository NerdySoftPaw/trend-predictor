# Trend Predictor

[![GitHub Release](https://img.shields.io/github/v/release/NerdySoftPaw/trend-predictor?style=flat-square)](https://github.com/NerdySoftPaw/trend-predictor/releases)
[![HACS Validation](https://img.shields.io/github/actions/workflow/status/NerdySoftPaw/trend-predictor/hacs.yaml?label=HACS&style=flat-square)](https://github.com/NerdySoftPaw/trend-predictor/actions/workflows/hacs.yaml)
[![Code Quality](https://img.shields.io/github/actions/workflow/status/NerdySoftPaw/trend-predictor/lint.yaml?label=lint&style=flat-square)](https://github.com/NerdySoftPaw/trend-predictor/actions/workflows/lint.yaml)
[![Tests](https://img.shields.io/github/actions/workflow/status/NerdySoftPaw/trend-predictor/tests.yaml?label=tests&style=flat-square)](https://github.com/NerdySoftPaw/trend-predictor/actions/workflows/tests.yaml)
[![Docs](https://img.shields.io/readthedocs/trend-predictor?style=flat-square)](https://trend-predictor.readthedocs.io)
[![License](https://img.shields.io/github/license/NerdySoftPaw/trend-predictor?style=flat-square)](LICENSE)

A Home Assistant integration that predicts when any numeric sensor will reach a target value — based on its current trend.

No more manual calculation of "how long until my PV battery is empty". Set it up once and Home Assistant tells you.

**[→ Full Documentation](https://trend-predictor.readthedocs.io)**

---

## Features

- **Three sensors per instance** — time remaining (hours), rate of change per hour, and a concrete predicted timestamp
- **Linear regression** over a configurable time window — more robust than a simple first/last comparison
- **Recorder warm-start** — loads history from the HA database on startup, sensors are accurate immediately
- **Config Flow UI** — no YAML, configure everything through the Home Assistant interface
- **Reconfigurable** — change source entity, target value, or time window at any time via Options
- **English & German** — UI and documentation in both languages

## Use cases

| Scenario | Source entity | Target value |
|----------|--------------|-------------|
| PV battery empty | `sensor.battery_soc` (%) | `0` |
| PV battery full | `sensor.battery_soc` (%) | `100` |
| Cistern runs dry | `sensor.cistern_level` (%) | `0` |
| Heating oil low | `sensor.oil_tank_level` (l) | `200` |
| Basement gets cold | `sensor.basement_temp` (°C) | `10` |

## Sensors

| Sensor | Unit | Description |
|--------|------|-------------|
| Time remaining | `h` | Hours until the target value is reached |
| Rate of change | `<unit>/h` | Current rate of change per hour (negative = falling) |
| Predicted time | — | Exact timestamp when the target will be reached |

All sensors show `unavailable` when the trend is moving away from the target or there are fewer than 2 data points.

## Installation

### Via HACS

1. Open HACS → **Integrations** → top-right menu → **Custom repositories**
2. Add `https://github.com/NerdySoftPaw/trend-predictor` with category **Integration**
3. Search for **Trend Predictor** → **Download**
4. Restart Home Assistant

### Manual

Download `trend_predictor.zip` from the [latest release](https://github.com/NerdySoftPaw/trend-predictor/releases/latest), unpack into `config/custom_components/trend_predictor/`, restart HA.

## Setup

After restarting: **Settings → Devices & Services → Add Integration → Trend Predictor**

| Setting | Default | Description |
|---------|---------|-------------|
| Source entity | — | Any `sensor` or `input_number` |
| Target value | `0` | Value to predict (e.g. 0 = empty, 100 = full) |
| Time window | `30 min` | How much history to use for the regression |

Create one instance per sensor you want to monitor.

## Automation example

```yaml
automation:
  - alias: "Battery almost empty – warning"
    trigger:
      - platform: numeric_state
        entity_id: sensor.battery_soc_time_remaining
        below: 2
    action:
      - service: notify.mobile_app_my_phone
        data:
          title: "Battery almost empty"
          message: >
            {{ states('sensor.battery_soc_time_remaining') }} h remaining.
            Expected to run out at {{ states('sensor.battery_soc_predicted_time') }}.
```

More examples in the [documentation](https://trend-predictor.readthedocs.io/en/latest/automations/).

## Contributing

Pull requests are welcome. Please run `black` and `isort` before submitting.

## License

MIT
