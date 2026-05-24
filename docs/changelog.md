# Changelog

## 2026.5.24

- **Min/Max validation:** The UI now prevents entering a minimum value that is greater than or equal to the maximum value. Existing entries with swapped values are automatically corrected on the next HA restart.
- **Performance:** Regression calculation is now debounced (1 s) — rapidly updating sensors no longer trigger a full recalculation on every single state change.
- **Security:** All GitHub Actions pinned to exact commit SHAs; force-push of release tags removed from the release workflow.

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
