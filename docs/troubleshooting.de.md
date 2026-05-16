# Troubleshooting

## Sensor zeigt `unavailable`

Es gibt drei mögliche Ursachen:

**1. Zu wenig Datenpunkte**
Der Quellsensor hat sich innerhalb des Zeitfensters weniger als zweimal geändert. Das passiert z.B. kurz nach dem Start oder wenn der Sensor sehr selten aktualisiert wird. Warten, bis genug Verlauf vorhanden ist.

**2. Trend bewegt sich vom Ziel weg**
Wenn die Batterie gerade lädt und der Zielwert `0` ist, geht der Trend in die falsche Richtung — die Restzeit lässt sich nicht sinnvoll berechnen. Entweder den Zielwert anpassen oder eine zweite Instanz für das andere Ziel (z.B. `100`) anlegen.

**3. Quellsensor liefert keinen numerischen Wert**
`unknown`, `unavailable` oder Text-Zustände können nicht verarbeitet werden. Warten bis der Sensor wieder einen Zahlenwert liefert.

---

## Schätzung springt stark

Das Zeitfenster ist zu kurz und der Sensor schwankt stark (z.B. durch kurze Lastspitzen). Zeitfenster auf 60 oder 120 Minuten erhöhen, um eine stabilere Regression zu bekommen.

---

## Entität ist im Config Flow nicht auswählbar

Nur Entitäten vom Typ `sensor` und `input_number` werden angezeigt. Entities aus anderen Domains können als Workaround über einen Template-Sensor in den richtigen Typ umgewandelt werden.

---

## Integration taucht nach Neustart nicht auf

Prüfen ob das Verzeichnis `custom_components/trend_predictor/` korrekt in der HA-Konfiguration liegt und ob `manifest.json` vorhanden ist. HA-Logs unter **Einstellungen → System → Protokolle** geben genaue Fehlermeldungen aus.

---

## Recorder-Verlauf wird nicht geladen

Die Integration benötigt die `recorder`-Integration (standardmäßig aktiv in HA). Falls der Recorder deaktiviert ist, startet Trend Predictor ohne Verlauf und sammelt Daten erst ab der ersten Zustandsänderung.
