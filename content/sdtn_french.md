## Visualisation des Journées d'Été et des Nuits Tropicales

---

## Vue d'ensemble

Analysez la distribution des **Journées d'Été** et des **Nuits Tropicales** en fonction de seuils de température personnalisables.

- **Journées d'Été** : Jours où la **température maximale journalière** dépasse **30 °C**.
  - $T_{max} > 30$
- **Nuits Tropicales** : Nuits où la **température minimale journalière** dépasse **20 °C**.
  - $T_{min} > 20$
- Ces seuils sont définis par défaut, mais la distribution et l'ampleur peuvent changer considérablement si d'autres seuils sont utilisés. N'hésitez pas à explorer !

Ces indicateurs sont largement utilisés par des organisations telles que **The Lancet** ou **MétéoSuisse** pour comprendre les impacts des vagues de chaleur et du changement climatique.

---

## Notes sur les Données

### Biais de Température
- **Biais diurne** : Un **biais constant de 1 à 1,5 °C** est souvent observé pendant la journée.
- **Biais nocturne** : Le biais nocturne est généralement plus faible mais peut atteindre **0,5 °C**.

### Données Manquantes
- Plusieurs stations ont des données incomplètes, ce qui peut affecter les résultats :
  - **Stations concernées** : 230, 231, 239, 214, et 240.
  - **Périodes critiques** : La station **230** manque de données pendant la **période cruciale de vague de chaleur estivale**, où la plupart des nuits tropicales et des nombreuses journées d'été se sont produites.

---

## Fonctionnalités de Visualisation

1. **Carte interactive** :
   - Affiche le nombre total de **journées d'été** ou de **nuits tropicales** à chaque station.
   - Les stations sont codées par couleur en fonction de leurs comptages d'excédence.

2. **Histogramme** :
   - Montre la distribution des comptages d'excédence pour toutes les stations.
   - Souligne la variabilité du nombre de jours dépassant le seuil choisi.

3. **Seuils Ajustables** :
   - Les seuils peuvent être ajustés dynamiquement via un curseur pour explorer différentes définitions des **journées d'été** et des **nuits tropicales**.

---
