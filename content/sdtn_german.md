## Visualisierung von Sommertagen und Tropennächten

---

## Überblick

Analysieren Sie die Verteilung von **Sommertagen** und **Tropennächten** basierend auf anpassbaren Temperaturschwellen.

- **Sommertage**: Tage, an denen die **tägliche Höchsttemperatur** über **30 °C** liegt.
  - $T_{max} > 30$
- **Tropennächte**: Nächte, in denen die **tägliche Mindesttemperatur** über **20 °C** liegt.
  - $T_{min} > 20$
- Diese Standardschwellenwerte können angepasst werden; die Verteilung und Größenordnung können sich je nach gewähltem Schwellenwert erheblich ändern. Erkunden Sie die Möglichkeiten!

Diese Indikatoren werden häufig von Organisationen wie **The Lancet** oder **MeteoSwiss** verwendet, um die Auswirkungen von Hitzewellen und Klimawandel zu bewerten.

---

## Datenhinweise

### Temperaturbias
- **Tagesbias**: Ein konsistenter **Bias von 1 bis 1,5 °C** wird tagsüber häufig beobachtet.
- **Nachtbias**: Der Nachtbias ist in der Regel kleiner, kann aber bis zu **0,5 °C** betragen.

### Fehlende Daten
- Einige Stationen haben unvollständige Daten, was die Ergebnisse beeinflussen kann:
  - **Betroffene Stationen**: 230, 231, 239, 214 und 240.
  - **Kritische Lücken**: Station **230** hat keine Daten während der **entscheidenden Hitzewellenperiode**, in der die meisten Tropennächte und viele Sommertage auftraten.

---

## Visualisierungsfunktionen

1. **Interaktive Karte**:
   - Zeigt die Gesamtzahl der **Sommertage** oder **Tropennächte** für jede Station.
   - Stationen sind farblich nach ihren Überschreitungswerten codiert.

2. **Histogramm**:
   - Zeigt die Verteilung der Überschreitungswerte für alle Stationen.
   - Hebt die Variabilität in der Anzahl der Tage hervor, die den gewählten Schwellenwert überschreiten.

3. **Anpassbare Schwellenwerte**:
   - Schwellenwerte können dynamisch über einen Schieberegler angepasst werden, um verschiedene Definitionen von **Sommertagen** und **Tropennächten** zu erkunden.

---
