# Changelog

## 2026.5.16.1

- **Auto direction detection:** No more fixed target value — configure a minimum and maximum instead. The integration picks the right target automatically based on trend direction (falling → min, rising → max)
- Active target exposed as `target` attribute on time remaining and predicted time sensors

## 2026.5.16

Initial release.

- Three sensors per instance: time remaining, rate of change, predicted time
- Linear regression (least squares) over a configurable time window
- Automatic history loading from the HA Recorder on startup
- Config Flow UI: source entity, target value, time window
- Reconfiguration via Options flow
- Translations: English, German
