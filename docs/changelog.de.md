# Changelog

## 2026.5.24

- **Min/Max-Validierung:** Die Benutzeroberfläche verhindert nun die Eingabe eines Minimalwerts, der größer oder gleich dem Maximalwert ist. Bereits gespeicherte Einträge mit vertauschten Werten werden beim nächsten HA-Neustart automatisch korrigiert.
- **Performance:** Die Regressionsberechnung wird jetzt per Debounce (1 s) gebündelt — schnell aktualisierte Sensoren lösen nicht mehr bei jedem einzelnen State-Change eine vollständige Neuberechnung aus.
- **Sicherheit:** Alle GitHub Actions auf exakte Commit-SHAs gepinnt; Force-Push von Release-Tags aus dem Release-Workflow entfernt.

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
