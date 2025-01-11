"""
Module: structure
==================

This module provides utility functions for managing file paths, language dictionaries,
and markdown loading. These utilities support the data processing and visualization
in the application.

Functions:
- get_files
- get_lang_dict
- load_markdown
"""


import streamlit as st
from pathlib import Path
from content.lang_dict import eng_dict, de_dict, fr_dict

CONTENT_DIR = Path.cwd() / "content"

def get_files(city: str, period: str) -> tuple:
    """
    Retrieve file paths for data files based on the selected city and period.

    Parameters:
    city : str
        Name of the city ('bern' or 'biel').
    period : str
        Time period ('Main Heatwave' or other periods).

    Returns:
    tuple
        Paths for land use, Fitnah, UHI, temperature stats, and SD/TN files.
    """

    fitnah_path = Path.cwd() / 'data' / city / 'data_viz_fitnah.csv'
    landuse_path = Path.cwd() / 'data' / city / 'data_viz_land_use.csv'

    if (period == 'Main Heatwave') | (period == 'Principale vague de chaleur') | (period == 'Haupt-Hitzewelle'):
        hw = True
    else:
        hw = False

    if city == 'bern':
        if hw:
            uhi_path = Path.cwd() / 'data' / city / 'heatwave_22_hourly_uhi_ci.csv'
            tempstats = Path.cwd() / 'data' / city / 'heatwave_22_temp_stats.csv'
            sdtn = Path.cwd() / 'data' / city / 'heatwave_22_sdtn.csv'
        else:
            uhi_path = Path.cwd() / 'data' / city / 'summer22_hourly_uhi_cis.csv'
            tempstats = Path.cwd() / 'data' / city / 'summer22_temp_stats.csv'
            sdtn = Path.cwd() / 'data' / city / 'summer22_sdtn.csv'

    if city == 'biel':
        if hw:
            uhi_path = Path.cwd() / 'data' / city / 'heatwave_23_hourly_uhi_ci.csv'
            tempstats = Path.cwd() / 'data' / city / 'heatwave_23_temp_stats.csv'
            sdtn = Path.cwd() / 'data' / city / 'heatwave_23_sdtn.csv'

        else:
            uhi_path = Path.cwd() / 'data' / city / 'summer23_hourly_uhi_ci.csv'
            tempstats = Path.cwd() / 'data' / city / 'summer23_temp_stats.csv'
            sdtn = Path.cwd() / 'data' / city / 'summer23_sdtn.csv'



    return landuse_path, fitnah_path, uhi_path, tempstats, sdtn


def get_lang_dict() -> dict:
    """
    Get the language dictionary based on the user's selection.

    Returns:
    dict
        Language dictionary for the selected language (EN, DE, or FR).
    """

    lang = st.selectbox('Choose Language / choisir langue / Sprache wählen', ['DE', 'EN', 'FR'])
    if lang == 'DE':
        return de_dict
    if lang == 'EN':
        return eng_dict
    if lang == 'FR':
        return fr_dict


def load_markdown(file_path: Path) -> str:
    """
    Load the content of a markdown file.

    Parameters:
    file_path : Path
        Path to the markdown file.

    Returns:
    str
        Content of the markdown file as a string, or an error message if the file is not found.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_path.name} not found."

sensor_labels = {
    206: 'rural reference',
    228: 'Südstrasse',
    217: 'Geyisreid',
    205: 'Ile de la Suze',
    221: 'Champagne-Piano',
    227: 'Altersheim-redenweg',
    216: 'Nidau-mittestrasse',
    211: 'Mühlefeld',
    226: 'Port Thielle',
    213: 'Port NBK',
    235: 'Altersheim-Reid',
    225: 'Swisstennis',
    207: 'Swiss Meteo Reference',
    237: 'Rolex',
    236: 'Taubenloch',
    224: 'Bözingen',
    234: 'Bözingenfeld',
    223: 'Altersheim-erlacher',
    240: 'Längholz-replacement',
    214: 'Längholz',
    208: 'Möösli',
    220: 'Altersheim-Neumarkt',
    219: 'New City',
    238: 'Museum',
    232: 'Champagne-Blumen',
    215: 'Old City',
    222: 'Spital',
    204: 'Stadtpark',
    230: 'Vingelz',
    201: 'Robert-Walser-Platz',
    233: 'Madretsch-Zukunft',
    218: 'Bahnhof',
    212: 'Seepark',
    210: 'Congresshaus',
    209: 'Madrestch-Piano',
    229: 'Viaductstrasse',
    203: 'Zentralplatz',
    231: 'Nidau-Lac',
    239: 'Nidau-wald',
    202: 'Hafen'
}