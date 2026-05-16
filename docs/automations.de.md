# Automationen

Fertige Beispiel-Automationen zum Kopieren und Anpassen.

## Benachrichtigung wenn Batterie bald leer

Sendet eine Nachricht, wenn der Akku noch weniger als 2 Stunden Restlaufzeit hat — aber nur einmal pro Abend.

```yaml
automation:
  - alias: "Batterie fast leer - Warnung"
    trigger:
      - platform: numeric_state
        entity_id: sensor.batterie_soc_restzeit
        below: 2
    condition:
      - condition: time
        after: "17:00:00"
        before: "23:00:00"
    action:
      - service: notify.mobile_app_mein_handy
        data:
          title: "Batterie fast leer"
          message: >
            Noch {{ states('sensor.batterie_soc_restzeit') }} h Restlaufzeit.
            Voraussichtlich leer um
            {{ states('sensor.batterie_soc_voraussichtlicher_zeitpunkt') }}.
```

## TTS-Ansage wenn PV-Batterie in unter einer Stunde voll

```yaml
automation:
  - alias: "Batterie fast voll - Ansage"
    trigger:
      - platform: numeric_state
        entity_id: sensor.batterie_soc_restzeit
        below: 1
    condition:
      - condition: numeric_state
        entity_id: sensor.batterie_soc
        above: 50
    action:
      - service: tts.speak
        target:
          entity_id: tts.piper
        data:
          message: "Die Batterie ist in weniger als einer Stunde vollgeladen."
```

## Dashboard-Karte mit allen drei Sensoren

```yaml
type: entities
title: PV-Batterie Vorhersage
entities:
  - entity: sensor.batterie_soc
    name: Aktueller Ladestand
  - entity: sensor.batterie_soc_aenderungsrate
    name: Änderungsrate
  - entity: sensor.batterie_soc_restzeit
    name: Restzeit
  - entity: sensor.batterie_soc_voraussichtlicher_zeitpunkt
    name: Voraussichtlich leer um
```

## Bedingte Karte (nur anzeigen wenn Restzeit bekannt)

```yaml
type: conditional
conditions:
  - entity: sensor.batterie_soc_restzeit
    state_not: unavailable
card:
  type: stat
  entity: sensor.batterie_soc_restzeit
  name: Restzeit bis leer
  unit: h
```
