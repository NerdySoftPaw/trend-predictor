# Troubleshooting

## Sensor shows `unavailable`

There are three possible causes:

**1. Not enough data points**
The source sensor has changed fewer than twice within the time window. This happens shortly after startup or when the sensor updates very infrequently. Wait until enough history has accumulated.

**2. Trend is moving away from the target**
If the battery is charging while the target value is `0`, the trend is going in the wrong direction — the time remaining cannot be calculated. Either adjust the target value or create a second instance for the other direction (e.g. target `100`).

**3. Source sensor is not providing a numeric value**
States like `unknown`, `unavailable` or text values cannot be processed. Wait until the sensor returns a numeric value again.

---

## Estimate is jumping around

The time window is too short and the sensor fluctuates strongly (e.g. due to short load spikes). Increase the time window to 60 or 120 minutes to get a more stable regression.

---

## Entity is not selectable in the config flow

Only entities of type `sensor` and `input_number` are shown. Entities from other domains can be wrapped in a template sensor as a workaround.

---

## Integration does not appear after restart

Check that the `custom_components/trend_predictor/` directory is in the correct location and that `manifest.json` is present. HA logs under **Settings → System → Logs** provide detailed error messages.

---

## Recorder history is not loaded

The integration requires the `recorder` integration (enabled by default in HA). If the Recorder is disabled, Trend Predictor starts without history and collects data from the first state change onwards.
