"""
Module: main.py
================

This module serves as the main entry point for the "Hot Biel Summer" app. It orchestrates
the functionality of visualizing geospatial and temporal data using Streamlit and the custom
modules defined in this project.

Functions:
- main: Sets up the app interface and coordinates the tabs for data visualization.
- uhi_city_index: Visualizes Urban Heat Island and City Index data using maps and histograms.
- tn_sd: Visualizes Summer Days and Tropical Nights data with adjustable thresholds.
- hourly_evolution: Displays the hourly evolution of UHI or City Index values.
- fitnah_tab: Renders visualizations of Fitnah data using maps and histograms.
- tab_explore_geodata: Explores geospatial data for selected buffers and types.

"""


import streamlit as st
import pandas as pd
from pathlib import Path
import ast
from modules.maps import plot_geodata, plot_fitnah_map, plot_uhi_ci_map, sdtn_map
from modules.plots import geodata_histogram, plot_fitnah_histogram, plot_uhi_ci_histogram, tn_sd_histogram, plot_uhi_ci_evolution
from modules.structure import get_files, get_lang_dict, load_markdown


# -------------------------------------------------------------------
# 1) App Setup
# -------------------------------------------------------------------


def main() -> None:
    """
    Sets up the Streamlit app interface and coordinates all visualization tabs.

    Returns:
    None
    """

    st.set_page_config(
        page_title="Hot Biel Summer",
        page_icon="🌞",
        layout="wide"
    )
    langdict = get_lang_dict()
    st.title(langdict['welcome_t'])
    st.markdown(langdict['welcome_message'])
    m1, m2, m3 = st.columns([1,1,2])
    with m1:
        city = st.radio(langdict['city'], ['biel', 'bern'], horizontal=True)
    with m2:
        period = st.radio(langdict['period'], langdict['period_choice'], horizontal=True)
    with m3:
        basemap = st.radio(langdict['basemap'], langdict['map_choice'], horizontal=True)
    st.info(langdict['date_info'])
    lu_path, f_path, u_path, tpath, spath = get_files(city, period)
    year = '23' if city == 'biel' else '22'
    sdtn_path = Path.cwd() / 'data' / city / f'summer{year}_sdtn.csv'

    # Create tabs

    tab_station_map, tab_tn_sd, tab_geo_map, tab_hourly_evolution, tab_fitnah_map, tab_explanation = st.tabs(langdict['tabs'])

    # -------------------------------------------------------------------
    # 2) Hourly Data
    # -------------------------------------------------------------------

    with tab_station_map:
        uhi_city_index(u_path, basemap, langdict)

    with tab_tn_sd:
        tn_sd(sdtn_path, tpath, basemap, langdict)
    st.subheader(langdict['uhi_title'])

    with tab_geo_map:
        tab_explore_geodata(lu_path, basemap, langdict)

    with tab_hourly_evolution:
        hourly_evolution(u_path, langdict)

    with tab_fitnah_map:
        fitnah_tab(f_path, basemap, langdict)

    with tab_explanation:
        st.markdown(load_markdown(langdict['welcome_md']))


def uhi_city_index(
    uhi_path: Path,
    basemap: str,
    langdict: dict,
) -> None:
    """
    Visualizes Urban Heat Island (UHI) and City Index data using maps and histograms.

    Parameters:
    uhi_path : Path
        Path to the CSV file containing UHI data.
    basemap : str
        The basemap to use for visualization.
    langdict : dict
        Language dictionary for localization.

    Returns:
    None
    """

    with st.expander(langdict['uhi_md_t']):
        st.markdown(load_markdown(langdict['uhi_md']))
    u1, u2 = st.columns(2)
    # Select Data Type (UHI or City Index)
    with u1:
        data_type = st.radio(langdict['dtype_uhi'], ['city_index', 'uhi'], key="data_type_selector", horizontal=True)
    # Visualization mode selection
    with u2:
        hour = st.slider(langdict['Hour'], min_value=0, max_value=23, step=1, key="hour_selector")

    uhi_ci_data = pd.read_csv(uhi_path)
    selected_data = uhi_ci_data[uhi_ci_data['hour'] == hour]

    ucol1, ucol2 = st.columns([2, 1])
    with ucol1:
        hour_str = str(hour)
        if len(hour_str) == 1:
            hour_str = '0' + hour_str
        st.markdown(f"##### {data_type.capitalize()} - {hour_str}:00")
        plot_uhi_ci_map(selected_data, data_type, hour, basemap)
    with ucol2:
        plot_uhi_ci_histogram(selected_data, data_type, hour_str, langdict)


def tn_sd(
    sdtn_path: Path,
    daily_stats_path: Path,
    basemap: str,
    langdict: dict,
) -> None:
    """
    Visualizes Summer Days and Tropical Nights data with adjustable temperature thresholds.

    Parameters:
    sdtn_path : Path
        Path to the CSV file containing Summer Days and Tropical Nights data.
    daily_stats_path : Path
        Path to the CSV file containing daily temperature statistics.
    basemap : str
        The basemap to use for visualization.
    langdict : dict
        Language dictionary for localization.

    Returns:
    None
    """

    daily_data = pd.read_csv(daily_stats_path)
    sdtn_data = pd.read_csv(sdtn_path)
    sdtn_geo = daily_data.merge(sdtn_data[['Name', 'logger', 'x', 'y']], how='left', on='logger')
    with st.expander(langdict['sdtn_md_t']):
        st.markdown(load_markdown(langdict['sdtn_md']))
    s1, s2 = st.columns([2, 1])
    with s1:
        metric = st.radio(
            langdict['dtype_tnsd'],
            [langdict['sdays_selection'], langdict['nights_selection']],
            horizontal=True
        )

        if metric == langdict['sdays_selection']:
            threshold_label = langdict['sdays_select']
            default_threshold = 30
            data_col = "daily_max"
        else:
            threshold_label = langdict['nights_select']
            default_threshold = 20
            data_col = "daily_min"
    with s2:
        threshold = st.slider(
            threshold_label,
            min_value=0.0,
            max_value=50.0,
            value=float(default_threshold),
            step=0.5
        )

    tncol1, tncol2 = st.columns([2, 1])
    with tncol1:
        summary = sdtn_map(sdtn_geo, data_col, metric, threshold, basemap)
    with tncol2:
        tn_sd_histogram(summary, threshold, langdict)


def hourly_evolution(
    uhi_path: Path,
    langdict: dict,
) -> None:
    """
    Displays the hourly evolution of Urban Heat Island (UHI) or City Index values.

    Parameters:
    uhi_path : Path
        Path to the CSV file containing UHI or City Index data.
    langdict : dict
        Language dictionary for localization.

    Returns:
    None
    """

    station_data = pd.read_csv(uhi_path)
    h1, h2 = st.columns([1, 2])
    with h1:
        data_type = st.radio(langdict['dtype_uhi'], ["uhi", "city_index"], index=0)

    # 2) Multi-select for loggers
    with h2:
        selected_loggers = st.multiselect(
            langdict['Sensor'],
            options=sorted(station_data["logger"].unique()),
            default=[]
        )

    # 3) If user selects at least one logger, plot the line chart
    if selected_loggers:
        plot_uhi_ci_evolution(station_data, selected_loggers, data_type, langdict)
    else:
        st.info(langdict['uhi_warning'])

def fitnah_tab(
    fitnah_path: Path,
    basemap: str,
    langdict: dict,
) -> None:
    """
    Renders visualizations of Fitnah data using maps and histograms.

    Parameters:
    fitnah_path : Path
        Path to the CSV file containing Fitnah data.
    basemap : str
        The basemap to use for visualization.
    langdict : dict
        Language dictionary for localization.

    Returns:
    None
    """

    with st.expander(langdict['fitnah_md_t']):
        st.markdown(load_markdown(langdict['fitnah_md']))
    # Read in the data for the selected city
    fitnah_data = pd.read_csv(fitnah_path)

    # Convert 'geometry_coords' from string to list
    fitnah_data['geometry_coords'] = fitnah_data['geometry_coords'].apply(ast.literal_eval)
    f1, f2, f3 = st.columns(3)
    with f1:
        # Let the user choose buffer size and data type
        buffer_size = st.selectbox(langdict['buffer'], [10, 50, 100, 500], key = 'fitnah_buffer')
    with f2:
        dtype = st.selectbox(langdict['dtype_fitnah'], ['fitnah_ss', 'fitnah_sv', 'fitnah_temp', 'dem'])
    with f3:
        aggregator = st.selectbox(langdict['aggregator'],
                                  ['min', 'max', 'mean', 'count'])
    # Filter the data
    sel_fitnah_data = fitnah_data[
        (fitnah_data['buffer'] == buffer_size) &
        (fitnah_data['dtype'] == dtype)
        ]

    fcol1, fcol2 = st.columns([2, 1])

    with fcol1:
        st.markdown(f'#### {dtype} - {aggregator.capitalize()} - {buffer_size}m')
        plot_fitnah_map(sel_fitnah_data, aggregator, basemap)
    with fcol2:
        plot_fitnah_histogram(sel_fitnah_data, aggregator, dtype, buffer_size, langdict)




def tab_explore_geodata(
    landuse_path: Path,
    basemap: str,
    langdict: dict,
) -> None:
    """
    Explores geospatial data using selected buffers and data types.

    Parameters:
    landuse_path : Path
        Path to the CSV file containing land use data.
    basemap : str
        The basemap to use for visualization.
    langdict : dict
        Language dictionary for localization.

    Returns:
    None
    """

    st.subheader(langdict['geo_title'])

    landuse = pd.read_csv(landuse_path)
    g1, g2 = st.columns(2)
    with g1:
        landuse_type = st.selectbox(langdict['dtype_landuse'], langdict['description_dict'].values())
    with g2:
        buffer = st.selectbox(langdict['buffer'], landuse['buffer'].unique(), key='geodata_buffer')
    sel_data = landuse[landuse['buffer'] == buffer]

    geo1, geo2 = st.columns([2,1])
    with geo1:
        plot_geodata(sel_data, landuse_type, basemap, langdict)
    with geo2:
        geodata_histogram(sel_data, landuse_type, buffer, langdict)


# 6) Entry Point
# -------------------------------------------------------------------
if __name__ == "__main__":
    main()
