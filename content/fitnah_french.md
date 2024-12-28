Les données FITNAH proviennent d'une grille raster de **10x10 mètres** de données sur les îlots de chaleur urbains (UHI) à 5h00 du matin, modélisées par l’entreprise allemande **Geonet** sous commande du **Canton de Berne**.

## Aperçu des données
Le modèle fournit :
1. **UHI Espace (fitnah_ss)** : Données UHI pour les espaces ouverts.
2. **UHI Rue (fitnah_sv)** : Données UHI pour les rues.
3. **Couche de température** : Utilisée pour calculer les couches UHI.

Les couches **UHI Espace** et **UHI Rue** sont accessibles au public, tandis que la couche de température est propriétaire. Pour plus de détails, consultez ma thèse ou les rapports de Geonet, disponibles pour de nombreux cantons suisses.

## Agrégation des données
Pour chaque station, les données raster de la zone environnante (dans un rayon défini) sont agrégées en utilisant :
- **Min**, **Max**, **Moyenne**, **Médiane** et **Compte**.

Le **Compte** est particulièrement important car les couches UHI Espace et UHI Rue ont souvent peu de cellules valides.

Cette agrégation est utile pour comparer les **données empiriques** des stations avec les **données UHI modélisées**.

## Note sur le Zoom
Veuillez noter que vous devez zoomer pour voir les buffers de 10 mètres - il peut sembler que rien n’apparaît !
