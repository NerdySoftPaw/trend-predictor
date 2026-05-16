# Automations

Ready-to-use automation examples — copy and adapt as needed.

## Notification when battery is almost empty

Sends a push notification when the battery has less than 2 hours of runtime left — but only once per evening.

```yaml
automation:
  - alias: "Battery almost empty – warning"
    trigger:
      - platform: numeric_state
        entity_id: sensor.battery_soc_time_remaining
        below: 2
    condition:
      - condition: time
        after: "17:00:00"
        before: "23:00:00"
    action:
      - service: notify.mobile_app_my_phone
        data:
          title: "Battery almost empty"
          message: >
            {{ states('sensor.battery_soc_time_remaining') }} h remaining.
            Expected to run out at
            {{ states('sensor.battery_soc_predicted_time') }}.
```

## TTS announcement when PV battery is almost full

```yaml
automation:
  - alias: "Battery almost full – announcement"
    trigger:
      - platform: numeric_state
        entity_id: sensor.battery_soc_time_remaining
        below: 1
    condition:
      - condition: numeric_state
        entity_id: sensor.battery_soc
        above: 50
    action:
      - service: tts.speak
        target:
          entity_id: tts.piper
        data:
          message: "The battery will be fully charged in less than one hour."
```

## Dashboard card with all three sensors

```yaml
type: entities
title: PV Battery Prediction
entities:
  - entity: sensor.battery_soc
    name: Current charge level
  - entity: sensor.battery_soc_rate_of_change
    name: Rate of change
  - entity: sensor.battery_soc_time_remaining
    name: Time remaining
  - entity: sensor.battery_soc_predicted_time
    name: Expected to run out at
```

## Conditional card (only show when time remaining is known)

```yaml
type: conditional
conditions:
  - entity: sensor.battery_soc_time_remaining
    state_not: unavailable
card:
  type: stat
  entity: sensor.battery_soc_time_remaining
  name: Time until empty
  unit: h
```
