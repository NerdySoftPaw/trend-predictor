# Trend Predictor

Trend Predictor ist eine Home Assistant Integration, die für jeden numerischen Sensor vorhersagt, wann er einen bestimmten Zielwert erreichen wird — basierend auf dem aktuellen Verlauf.

## Wie es funktioniert

Die Integration beobachtet einen Sensor (z.B. Batterie-SOC in Prozent), analysiert den Verlauf über ein konfigurierbares Zeitfenster und berechnet mittels linearer Regression, wann der Sensor einen eingestellten Zielwert erreicht.

## Die drei Sensoren

| Sensor | Beispielwert | Beschreibung |
|--------|-------------|--------------|
| **Restzeit** | `4.2 h` | Stunden bis der Zielwert erreicht wird |
| **Änderungsrate** | `-3.5 %/h` | Aktuelle Änderungsrate pro Stunde |
| **Voraussichtlicher Zeitpunkt** | `2026-05-16 20:30` | Konkreter Zeitpunkt als Timestamp |

Alle drei Sensoren zeigen `unavailable`, wenn der Trend gerade in die falsche Richtung geht oder zu wenig Datenpunkte vorliegen.

## Typische Anwendungsfälle

- **PV-Batterie leer:** Wann ist der Akku bei aktuellem Verbrauch auf 0%?
- **PV-Batterie voll:** Wann ist der Akku bei aktueller Ladung auf 100%?
- **Zisterne:** Wann ist der Wassertank bei aktuellem Verbrauch leer?
- **Heizöltank:** Vorausschauende Bestellung bevor der Tank leer ist
- **Temperatursensor:** Wann kühlt der Keller auf eine kritische Temperatur ab?

## Quick Start

!!! tip "In 3 Schritten eingerichtet"
    1. Trend Predictor über HACS installieren
    2. Home Assistant neu starten
    3. Einstellungen → Geräte & Dienste → Integration hinzufügen → **Trend Predictor**

→ [Installationsanleitung](installation.md)
