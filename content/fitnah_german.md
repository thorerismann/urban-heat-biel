Die FITNAH-Daten stammen aus einem **10x10-Meter-Raster** der Urban Heat Island (UHI)-Daten um 5:00 Uhr morgens in zwei Metern Höhe. Diese wurden von der deutschen Firma **Geonet** im Auftrag des **Kantons Bern** modelliert.

Den Bericht (auf Deutsch) von GeoNet und dem Kanton Bern finden Sie [hier](https://geofiles.be.ch/geoportal/pub/lpi/KLIMAMODELL_BE_Bericht_DE.pdf).

## Nutzung
1) Wählen Sie den anzuzeigenden Datentyp aus:
 - **UHI Freiflächen (fitnah_ss)**: UHI-Daten für Freiflächen.
 - **UHI Straßen (fitnah_sv)**: UHI-Daten für Straßen.
 - **Temperaturschicht**: Wird zur Berechnung der UHI-Schichten verwendet.

Die **UHI Freiflächen**- und **UHI Straßen**-Schichten sind öffentlich verfügbar, während die Temperaturschicht proprietär ist. Für weitere Details konsultieren Sie meine Thesis oder die Berichte von Geonet, die für zahlreiche Schweizer Kantone verfügbar sind.

## Datenaggregation
Für jede Station werden die Rasterdaten aus der Umgebung (innerhalb eines definierten Puffers) aggregiert mittels:
- **Min**, **Max**, **Mittelwert**, **Median** und **Anzahl**.

Die **Anzahl** ist besonders wichtig, da die Schichten **UHI Freiflächen** und **UHI Straßen** oft nur begrenzte gültige Zellen enthalten.

Diese Aggregation ist nützlich, um die **empirischen Daten** der Stationen mit den **modellierten UHI-Daten** zu vergleichen.

## Zoom-Hinweis
Bitte beachten Sie, dass Sie heranzoomen müssen, um die 10-Meter-Puffer zu sehen – es mag zunächst leer erscheinen! Die Puffer sind maßstabsgetreu dargestellt, um einen Eindruck von der Größe des Datenaggregationsbereichs zu vermitteln.
