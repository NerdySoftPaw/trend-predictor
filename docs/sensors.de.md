# Sensoren

Pro konfigurierter Instanz werden drei Sensoren angelegt, alle unter einem gemeinsamen Gerät gruppiert.

## Übersicht

| Sensor | Einheit | Device Class | State Class |
|--------|---------|--------------|-------------|
| Restzeit | `h` | — | Measurement |
| Änderungsrate | `<einheit>/h` | — | Measurement |
| Voraussichtlicher Zeitpunkt | — | `timestamp` | — |

---

## Restzeit

Gibt an, wie viele Stunden es bei aktuellem Trend dauert, bis der aktive Zielwert (Minimum oder Maximum, je nach Richtung) erreicht wird.

- Einheit: `h` (Stunden, als Dezimalzahl — z.B. `4.2`)
- Für Minuten-Darstellung im Dashboard: `{{ (states('sensor.xyz_restzeit') | float * 60) | round }} min`
- Zeigt `unavailable` wenn:
    - Weniger als 2 Datenpunkte im Zeitfenster
    - Der Quellsensor keinen numerischen Wert liefert
    - Die Rate genau null ist (kein Trend erkennbar)
- **Attribut `target`:** Welcher Wert gerade angesteuert wird (Min oder Max)

## Änderungsrate

Die aktuelle Änderungsrate des Quellsensors pro Stunde, berechnet per linearer Regression.

- Einheit: dynamisch — `%/h` wenn der Quellsensor `%` als Einheit hat, sonst `<einheit>/h`
- Negativ = Wert fällt → Integration steuert den **Minimalwert** an
- Positiv = Wert steigt → Integration steuert den **Maximalwert** an

## Voraussichtlicher Zeitpunkt

Der konkrete Zeitpunkt, zu dem der aktive Zielwert voraussichtlich erreicht wird — als Timestamp-Sensor.

- Device Class: `timestamp` → HA formatiert ihn automatisch als Datum/Uhrzeit
- Verwendbar in Automationen direkt als Zeitpunkt-Trigger
- Zeigt `unavailable` unter den gleichen Bedingungen wie die Restzeit
- **Attribut `target`:** Welcher Wert gerade angesteuert wird

---

## Wie die Richtungserkennung funktioniert

Das Ziel wird automatisch anhand der Regressionssteigung gewählt:

```
Rate < 0  →  Ziel = Minimalwert  (z.B. 0)
Rate > 0  →  Ziel = Maximalwert  (z.B. 100)

Restzeit = (Ziel − aktueller Wert) / Rate
```

Wenn eine PV-Batterie von Entladen auf Laden wechselt, ändert sich das Vorzeichen der Rate und Ziel sowie Vorhersage aktualisieren sich automatisch — keine Neukonfiguration nötig.

---

## Wie die Berechnung funktioniert

Die Integration sammelt alle Zustandsänderungen des Quellsensors innerhalb des konfigurierten Zeitfensters und berechnet daraus per **linearer Regression** (kleinste Quadrate) die Trendgerade. Aus aktuellem Wert, Steigung und aktivem Ziel ergibt sich die Restzeit.

Lineare Regression über mehrere Punkte ist robuster als die einfache Differenz zwischen erstem und letztem Wert, weil kurzfristige Ausreißer weniger Gewicht bekommen.
