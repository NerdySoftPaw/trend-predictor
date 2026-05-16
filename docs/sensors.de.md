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

Gibt an, wie viele Stunden es bei aktuellem Trend dauert, bis der Zielwert erreicht wird.

- Einheit: `h` (Stunden, als Dezimalzahl — z.B. `4.2`)
- Für Minuten-Darstellung im Dashboard: `{{ (states('sensor.xyz_restzeit') | float * 60) | round }} min`
- Zeigt `unavailable` wenn:
    - Weniger als 2 Datenpunkte im Zeitfenster
    - Der Trend sich vom Zielwert wegbewegt
    - Der Quellsensor keinen numerischen Wert liefert

## Änderungsrate

Die aktuelle Änderungsrate des Quellsensors pro Stunde, berechnet per linearer Regression.

- Einheit: dynamisch — `%/h` wenn der Quellsensor `%` als Einheit hat, sonst `<einheit>/h`
- Negativ = Wert fällt, Positiv = Wert steigt
- Nützlich zur Diagnose: z.B. `-3.5 %/h` bedeutet der Akku verliert 3,5% pro Stunde

## Voraussichtlicher Zeitpunkt

Der konkrete Zeitpunkt, zu dem der Zielwert voraussichtlich erreicht wird — als Timestamp-Sensor.

- Device Class: `timestamp` → HA formatiert ihn automatisch als Datum/Uhrzeit
- Verwendbar in Automationen direkt als Zeitpunkt-Trigger
- Zeigt `unavailable` unter den gleichen Bedingungen wie die Restzeit

---

## Wie die Berechnung funktioniert

Die Integration sammelt alle Zustandsänderungen des Quellsensors innerhalb des konfigurierten Zeitfensters und berechnet daraus per **linearer Regression** (kleinste Quadrate) die Trendgerade. Aus dem aktuellen Wert und der Steigung dieser Geraden ergibt sich die verbleibende Zeit bis zum Zielwert.

```
Restzeit (h) = (Zielwert − aktueller Wert) / Änderungsrate
```

Lineare Regression über mehrere Punkte ist robuster als die einfache Differenz zwischen erstem und letztem Wert, weil kurzfristige Ausreißer weniger Gewicht bekommen.
