# Été chaud à Bienne
Cette application visualise les données de la **campagne de mesure de l'été 2023 à Bienne**, de la **campagne de mesure de l'été 2022 à Berne**, ainsi que des données du modèle **FITNAH-3D UHI** et **des UHI de Berne**.

**Découvrez l'application de modélisation [ici](https://urbanheatmodel.streamlit.app/).**

UHI = Île de Chaleur Urbaine = La hausse des températures en milieu urbain due à l'environnement bâti.

### Sources de données
- **Données FITNAH** : Issues du modèle de température et d'UHI commandé par le canton de Berne en 2022.
- **Modèle Numérique de Terrain** : Provenant de SwissTopo Alti-3d via le plugin SwissGeoDownloader de QGIS.
- **Données des Stations et Résultats d'Indice de Chaleur à Bienne** : Collectées pendant la **campagne de mesures de 2023 à Bienne**.
- **Données des Stations et Résultats d'Indice de Chaleur à Berne** : Collectées pendant la **campagne de mesures de 2022 à Berne**.
- **Données Météorologiques** : Issues des trois stations automatiques SwissMetNet les plus proches de Bienne.
- **Couches cartographiques** : Accessibles via le WMTS de SwissTopo.
---

### Construit avec
- **Streamlit** : Cadre principal de l'application.
- **Plotly** : Pour des graphiques interactifs.
- **Geopandas**, **Rasterio**, **Shapely**, **Xarray**, **Numpy** : Utilisés pour la préparation des données.
---

### En savoir plus
- **Thèse complète** : Disponible une fois ma note finale reçue...
- **Données limitées de l'application** : Explorez le référentiel GitHub pour un sous-ensemble de données disponibles dans cette application.
- **Autre application** : Consultez l'autre application : [ici](https://urbanheatmodel.streamlit.app/).
---

### Retours bienvenus
Vous avez des commentaires, questions, suggestions ou critiques ? Je suis à l'écoute !

-TGE
