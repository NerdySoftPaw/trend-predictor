# Konfiguration

Die Konfiguration erfolgt vollständig über die Home Assistant UI — kein YAML erforderlich.

## Parameter

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|---------|--------------|
| **Quell-Entität** | Entity ID | — | Numerischer Sensor, dessen Verlauf analysiert wird |
| **Zielwert** | Zahl | `0` | Wert, zu dem die Vorhersage berechnet wird |
| **Zeitfenster** | Minuten | `30` | Wie viel Verlauf für die Berechnung genutzt wird |

## Quell-Entität

Es werden Entitäten vom Typ `sensor` und `input_number` unterstützt. Der aktuelle Zustand muss ein numerischer Wert sein (kein `unknown` oder `unavailable`).

## Zielwert

- Für "wann ist die Batterie leer?" → `0`
- Für "wann ist die Batterie voll?" → `100`
- Beliebige andere Werte möglich (z.B. Mindestfüllstand, kritische Temperatur)

## Zeitfenster

Das Zeitfenster bestimmt, wie viele Minuten Verlauf in die lineare Regression einfließen.

- **Kurzes Fenster (5–15 Min):** Reagiert schnell auf Verbrauchsänderungen, aber anfälliger für kurzfristige Schwankungen
- **Mittleres Fenster (30 Min):** Guter Kompromiss für die meisten Anwendungsfälle
- **Langes Fenster (60–120 Min):** Stabile Schätzung bei gleichmäßigem Verlauf, reagiert langsamer auf Änderungen

!!! tip
    Beim Start der Integration werden die letzten `n` Minuten automatisch aus der HA-Datenbank (Recorder) geladen. Die Sensoren sind also sofort nach dem Neustart aktiv.

## Nachträgliche Anpassung

Alle Parameter lassen sich jederzeit über **Einstellungen → Geräte & Dienste → Trend Predictor → Konfigurieren** ändern.
