# Changelog

## 2026.5.16.1

- **Automatische Richtungserkennung:** Kein fixer Zielwert mehr — stattdessen Minimal- und Maximalwert konfigurieren. Die Integration wählt den passenden Zielwert automatisch je nach Trend-Richtung (fallend → Min, steigend → Max)
- Aktives Ziel als `target`-Attribut am Restzeit- und Zeitpunkt-Sensor

## 2026.5.16

Erstes Release.

- Drei Sensoren pro Instanz: Restzeit, Änderungsrate, Voraussichtlicher Zeitpunkt
- Lineare Regression (kleinste Quadrate) über konfigurierbares Zeitfenster
- Automatisches Laden des Verlaufs aus dem HA-Recorder beim Start
- Config Flow UI: Quell-Entität, Zielwert, Zeitfenster
- Nachträgliche Anpassung über Optionen möglich
- Übersetzungen: Englisch, Deutsch
