# L'Été Chaud de Bienne

Cette application visualise les données de la **campagne de mesure estivale 2023 à Bienne/Biel**, ainsi que les **données du modèle FITNAH UHI** et les **données UHI de Berne**.

UHI = Urban Heat Island = Combien il fait plus chaud en ville à cause de l’environnement construit.

### Sources de données
- **Données FITNAH** : Issues du modèle UHI et de température commandé par le canton de Berne en 2022.
- **Modèle numérique d’altitude (DEM)** : Provenant du SwissTopo Alti-3d via le plugin SwissGeoDownloader disponible dans QGIS.
- **Données des stations et résultats de l’indice de chaleur à Bienne** : Recueillis lors de la **campagne de mesure estivale 2023 à Bienne**, menée par votre auteur avec le soutien significatif de l’Institut de géographie de l’Université de Berne (GIUB) et de la ville de Bienne.
- **Données des stations et résultats de l’indice de chaleur à Berne** : Recueillis lors de la **campagne de mesure estivale 2022 à Berne**, menée par le GIUB et la ville de Berne.
- **Données météorologiques** : Issues des trois stations météorologiques automatiques SwissMetNet les plus proches de Bienne.

---

### Développé avec
- **Streamlit** : Cadre principal de l’application.
- **Plotly** : Pour des graphiques interactifs.
- **PyDeck** : Pour des visualisations cartographiques dynamiques.
- **Geopandas**, **Rasterio**, **Shapely**, **Xarray**, **Numpy** : Utilisés pour la préparation des données.

---

### Pour en savoir plus
- **Thèse complète** : Disponible ici, avec méthodologie détaillée et analyses.
- **Référentiel de réplication** : Accédez à l’ensemble des données et scripts [ici](#).
- **Données limitées de l’application** : Explorez le référentiel GitHub pour le sous-ensemble de données disponible dans cette app.

---

### Vos retours
Des commentaires, questions, suggestions ou critiques ? Je serais ravi de vous lire !

-TGE
