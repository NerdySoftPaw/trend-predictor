# Installation

## Via HACS (empfohlen)

1. HACS in Home Assistant öffnen
2. **Integrationen** → Menü oben rechts → **Benutzerdefinierte Repositories**
3. URL `https://github.com/NerdySoftPaw/trend-predictor` eintragen, Kategorie **Integration**
4. Integration **Trend Predictor** suchen und **Herunterladen**
5. Home Assistant neu starten

Sobald Trend Predictor im HACS-Standardkatalog aufgenommen ist, entfällt Schritt 2–3.

## Manuelle Installation

1. Neueste Version von der [Releases-Seite](https://github.com/NerdySoftPaw/trend-predictor/releases) herunterladen (`trend_predictor.zip`)
2. ZIP-Inhalt in das Verzeichnis `config/custom_components/trend_predictor/` entpacken
3. Home Assistant neu starten

## Integration einrichten

Nach dem Neustart:

1. **Einstellungen** → **Geräte & Dienste** → **Integration hinzufügen**
2. Nach **Trend Predictor** suchen
3. Konfigurationsdialog ausfüllen (siehe [Konfiguration](configuration.md))

Pro Sensor, den du überwachen möchtest, legst du eine eigene Integration-Instanz an.
