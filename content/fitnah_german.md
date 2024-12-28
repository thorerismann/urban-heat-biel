Die FITNAH-Daten stammen aus einem **10x10 Meter Raster** von Urban Heat Island (UHI)-Daten, modelliert von der deutschen Firma **Geonet** im Auftrag des **Kantons Bern**. Die Daten beziehen sich auf 5:00 Uhr morgens.

## Datenübersicht
Das Modell liefert:
1. **UHI Fläche (fitnah_ss)**: UHI-Daten für offene Flächen.
2. **UHI Straße (fitnah_sv)**: UHI-Daten für Straßen.
3. **Temperatur-Schicht**: Zur Berechnung der UHI-Schichten.

Die Schichten **UHI Fläche** und **UHI Straße** sind öffentlich verfügbar, während die Temperatur-Schicht proprietär ist. Weitere Informationen finden Sie in meiner Arbeit oder in den Berichten von Geonet, die für zahlreiche Schweizer Kantone verfügbar sind.

## Datenaggregation
Für jede Station werden die Rasterdaten der umliegenden Region (innerhalb eines definierten Puffers) aggregiert nach:
- **Min**, **Max**, **Mittelwert**, **Median** und **Anzahl**.

Die **Anzahl** ist besonders wichtig, da die Schichten UHI Fläche und UHI Straße oft nur wenige gültige Zellen enthalten.

Diese Aggregation ist nützlich, um die **empirischen Daten** der Stationen mit den **modellenbasierten UHI-Daten** zu vergleichen.

## Hinweis zum Zoom
Bitte beachten Sie, dass Sie hineinzoomen müssen,
