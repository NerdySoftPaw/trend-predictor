# Konfiguration

Die Konfiguration erfolgt vollständig über die Home Assistant UI — kein YAML erforderlich.

## Parameter

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|---------|--------------|
| **Quell-Entität** | Entity ID | — | Numerischer Sensor, dessen Verlauf analysiert wird |
| **Minimalwert** | Zahl | `0` | Unterer Grenzwert – wird angesteuert wenn der Trend fällt |
| **Maximalwert** | Zahl | `100` | Oberer Grenzwert – wird angesteuert wenn der Trend steigt |
| **Zeitfenster** | Minuten | `30` | Wie viel Verlauf für die Berechnung genutzt wird |

## Quell-Entität

Es werden Entitäten vom Typ `sensor` und `input_number` unterstützt. Der aktuelle Zustand muss ein numerischer Wert sein (kein `unknown` oder `unavailable`).

## Automatische Richtungserkennung

Die Integration erkennt die Trend-Richtung automatisch und wählt den passenden Zielwert:

- **Trend fällt** (Rate < 0) → Vorhersage bis zum **Minimalwert**
- **Trend steigt** (Rate > 0) → Vorhersage bis zum **Maximalwert**

Kein manuelles Umschalten nötig. Wenn eine PV-Batterie entlädt, zeigen die Sensoren wann sie auf 0% fällt. Sobald sie lädt, wechseln sie automatisch auf die Vorhersage bis 100%.

Das aktuell aktive Ziel ist als `target`-Attribut am Restzeit- und Zeitpunkt-Sensor abrufbar.

## Zeitfenster

Das Zeitfenster bestimmt, wie viele Minuten Verlauf in die lineare Regression einfließen.

- **Kurzes Fenster (5–15 Min):** Reagiert schnell auf Verbrauchsänderungen, aber anfälliger für kurzfristige Schwankungen
- **Mittleres Fenster (30 Min):** Guter Kompromiss für die meisten Anwendungsfälle
- **Langes Fenster (60–120 Min):** Stabile Schätzung bei gleichmäßigem Verlauf, reagiert langsamer auf Änderungen

!!! tip
    Beim Start der Integration werden die letzten `n` Minuten automatisch aus der HA-Datenbank (Recorder) geladen. Die Sensoren sind also sofort nach dem Neustart aktiv.

## Nachträgliche Anpassung

Alle Parameter lassen sich jederzeit über **Einstellungen → Geräte & Dienste → Trend Predictor → Konfigurieren** ändern.
