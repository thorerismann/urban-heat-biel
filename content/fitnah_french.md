Les données FITNAH proviennent d'une **grille raster de 10x10 mètres** des données de l'île de chaleur urbaine (UHI) à 5h00 du matin à une hauteur de deux mètres, modélisées par la société allemande **Geonet** sous la commande du **Canton de Berne**.

Consultez le rapport (en allemand) de GeoNet et du Canton de Berne [ici](https://geofiles.be.ch/geoportal/pub/lpi/KLIMAMODELL_BE_Bericht_DE.pdf)

## Utilisation
1) Sélectionnez le type de données à afficher :
 - **UHI Espaces (fitnah_ss)** : Données UHI pour les espaces ouverts.
 - **UHI Rues (fitnah_sv)** : Données UHI pour les rues.
 - **Couche de Température** : Utilisée pour calculer les couches UHI.

Les couches **UHI Espaces** et **UHI Rues** sont disponibles publiquement, tandis que la couche de température est propriétaire. Pour plus de détails, consultez ma thèse ou les rapports de Geonet, disponibles pour de nombreux cantons suisses.

## Agrégation des données
Pour chaque station, les données raster de la zone environnante (dans un rayon défini) sont agrégées en utilisant :
- **Min**, **Max**, **Moyenne**, **Médiane**, et **Comptage**.

Le **Comptage** est particulièrement important car les couches UHI Espaces et UHI Rues ont souvent des cellules valides limitées.

Cette agrégation est utile pour comparer les **données empiriques** des stations avec les **données UHI modélisées**.

## Remarque sur le zoom
Notez que vous devez zoomer pour voir les tampons de 10 mètres - cela peut sembler vide sinon ! Les tampons sont mis à l'échelle réelle pour donner une impression de la taille de la zone d'agrégation des données.
