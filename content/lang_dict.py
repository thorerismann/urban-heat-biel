from pathlib import Path

CONTENT_DIR = Path.cwd() / "content"

eng_dict = {
    'fitnah_md_t': 'Show Fitnah Explanation',
    'landuse_md_t': 'Show Landuse Explanation',
    'uhi_md_t': 'Show UHI /City Index Explanation',
    'sdtn_md_t': 'Show Summer Days / Tropical Nights Explanation',
    'welcome_md_t': 'Show Instructions & Background',
    'welcome_md': CONTENT_DIR / 'welcome_en.md',
    'fitnah_md': CONTENT_DIR / 'fitnah_english.md',
    'landuse_md': CONTENT_DIR / 'landuse_english.md',
    'uhi_md': CONTENT_DIR / 'uhi_english.md',
    'sdtn_md': CONTENT_DIR / 'sdtn_english.md',
    'buffer': 'Select Buffer Radius',
    'Sensor': 'Select one or more loggers to plot',
    'Hour': 'Select Hour (24 hour format)',
    'dtype_uhi': 'Select UHI or City Index',
    'dtype_tnsd': 'Select Tropical Nights or Summer Days',
    'dtype_landuse': 'Select landuse type',
    'dtype_fitnah': 'Select fitnah datatype',
    'city': 'Select a city',
    'period': 'Select a period',
    'basemap': 'Select basemap',
    'date_info':'The Biel data is from May 15th - Sep 15th 2023 and the Bern data is from May 15th - Sep 15th 2022. The meanheatwave in Biel occured in in August 2023, while in Bern it was in July 2022.',
    'tabs': ["UHI & City Index", "Tropical Nights & Summer Days", "Landuse and Elevation", "Hourly Evolution of the UHI & City Index", "FITNAH Model"],
    'uhi_warning': 'Please select at least one logger to see the time evolution plot.',
    'fitnah_title': 'Fitnah Station Values',
    'uhi_title': 'UHI and City Index Visualization',
    'sdtn_title': 'Summer Days & Tropical Nights',
    'geo_title': 'Landuse Data',
    'uhi_hour_title': 'UHI Hourly Evolution',
    'aggregator': 'Select geospatial aggregator for visualization:',
    'period_choice': ['Whole summer', 'Main Heatwave'],
    'map_choice': ['Swiss National Map Color', 'Swiss National Map Grey'],
    'description_dict': {
        20: "Buildings",
        22: "Paved",
        14: "Water",
        7: "Rails",
        9: "Grass",
        15: "Vines",
        24: "Developed",
        25: "Forest",
        16: "Rock",
        27: "Barren"
    }
}

de_dict = {
    'fitnah_md_t': 'FITNAH-Erklärung anzeigen',
    'landuse_md_t': 'Landnutzungs-Erklärung anzeigen',
    'uhi_md_t': 'UHI-/Stadtindex-Erklärung anzeigen',
    'sdtn_md_t': 'Erklärung zu Sommertagen / Tropennächten anzeigen',
    'welcome_md_t': 'Anweisungen und Hintergrund anzeigen',

    # Correct German Markdown filenames
    'welcome_md': CONTENT_DIR / 'welcome_de.md',
    'fitnah_md': CONTENT_DIR / 'fitnah_german.md',
    'landuse_md': CONTENT_DIR / 'landuse_german.md',
    'uhi_md': CONTENT_DIR / 'uhi_german.md',
    'sdtn_md': CONTENT_DIR / 'sdtn_german.md',

    'buffer': 'Buffer-Radius auswählen',
    'Sensor': 'Wähle einen oder mehrere Logger aus',
    'Hour': 'Stunde auswählen (24-Stunden-Format)',
    'dtype_uhi': 'UHI oder Stadtindex auswählen',
    'dtype_tnsd': 'Tropennächte oder Sommertage auswählen',
    'dtype_landuse': 'Landnutzungstyp auswählen',
    'dtype_fitnah': 'FITNAH-Datentyp auswählen',
    'city': 'Stadt auswählen',
    'period': 'Zeitraum auswählen',
    'basemap': 'Basiskarte auswählen',
    'date_info': (
        'Die Biel-Daten stammen vom 15. Mai bis 15. September 2023, '
        'und die Bern-Daten stammen vom 15. Mai bis 15. September 2022. '
        'Die durchschnittliche Hitzewelle in Biel trat im August 2023 auf, '
        'während sie in Bern im Juli 2022 auftrat.'
    ),
    'tabs': [
        "UHI & Stadtindex",
        "Tropennächte & Sommertage",
        "Landnutzung und Höhe",
        "Stündliche Entwicklung von UHI & Stadtindex",
        "FITNAH-Modell"
    ],
    'uhi_warning': 'Bitte wählen Sie mindestens einen Logger aus, um das Zeitentwicklungsdiagramm anzuzeigen.',
    'fitnah_title': 'FITNAH-Stationenwerte',
    'uhi_title': 'Visualisierung von UHI und Stadtindex',
    'sdtn_title': 'Sommertage & Tropennächte',
    'geo_title': 'Landnutzungsdaten',
    'uhi_hour_title': 'Stündliche Entwicklung des UHI',
    'aggregator': 'Wählen Sie einen geospatialen Aggregator für die Visualisierung:',
    'period_choice': ['Ganzer Sommer', 'Haupt-Hitzewelle'],
    'map_choice': ['Schweizer Landeskarte Farbe', 'Schweizer Landeskarte Grau'],
    'description_dict':{
        20: "Gebäude",
        22: "Gepflastert",
        14: "Wasser",
        7: "Schienen",
        9: "Gras",
        15: "Reben",
        24: "Entwickelt",
        25: "Wald",
        16: "Felsen",
        27: "Ödland"
    }
}
fr_dict = {
    'fitnah_md_t': 'Afficher l’explication de FITNAH',
    'landuse_md_t': 'Afficher l’explication sur l’occupation du sol',
    'uhi_md_t': 'Afficher l’explication de l’UHI / Indice de la ville',
    'sdtn_md_t': 'Afficher l’explication sur les journées estivales / nuits tropicales',
    'welcome_md_t': 'Afficher les instructions et le contexte',

    # Correct French Markdown filenames
    'welcome_md': CONTENT_DIR / 'welcome_fr.md',
    'fitnah_md': CONTENT_DIR / 'fitnah_french.md',
    'landuse_md': CONTENT_DIR / 'landuse_french.md',
    'uhi_md': CONTENT_DIR / 'uhi_french.md',
    'sdtn_md': CONTENT_DIR / 'sdtn_french.md',

    'buffer': 'Sélectionner le rayon du buffer',
    'Sensor': 'Sélectionner un ou plusieurs enregistreurs à tracer',
    'Hour': 'Sélectionner l’heure (format 24 heures)',
    'dtype_uhi': 'Sélectionner UHI ou l’Indice de la ville',
    'dtype_tnsd': 'Sélectionner Nuits tropicales ou Journées estivales',
    'dtype_landuse': 'Sélectionner le type d’occupation du sol',
    'dtype_fitnah': 'Sélectionner le type de données FITNAH',
    'city': 'Sélectionner une ville',
    'period': 'Sélectionner une période',
    'basemap': 'Sélectionner la carte de base',
    'date_info': (
        'Les données de Bienne datent du 15 mai au 15 septembre 2023 et celles de Berne '
        'du 15 mai au 15 septembre 2022. La vague de chaleur moyenne à Bienne '
        's’est produite en août 2023, tandis qu’à Berne elle a eu lieu en juillet 2022.'
    ),
    'tabs': [
        "UHI & Indice de la ville",
        "Nuits tropicales & Journées estivales",
        "Occupation du sol et altitude",
        "Évolution horaire de l’UHI & de l’Indice de la ville",
        "Modèle FITNAH"
    ],
    'uhi_warning': 'Veuillez sélectionner au moins un enregistreur pour afficher le graphique d’évolution temporelle.',
    'fitnah_title': 'Valeurs des stations FITNAH',
    'uhi_title': 'Visualisation de l’UHI et de l’Indice de la ville',
    'sdtn_title': 'Journées estivales & Nuits tropicales',
    'geo_title': 'Données sur l’occupation du sol',
    'uhi_hour_title': 'Évolution horaire de l’UHI',
    'aggregator': 'Sélectionnez un agrégateur géospatial pour la visualisation :',
    'period_choice': ['Tout l’été', 'Principale vague de chaleur'],
    'map_choice': ['Carte nationale suisse en couleur', 'Carte nationale suisse en gris'],
    'description_dict': {
        20: "Bâtiments",
        22: "Pavé",
        14: "Eau",
        7: "Rails",
        9: "Herbe",
        15: "Vignes",
        24: "Développé",
        25: "Forêt",
        16: "Roche",
        27: "Nu"
    }


}