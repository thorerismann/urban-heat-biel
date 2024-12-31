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


def main():
    st.set_page_config(
        page_title="Hot Biel Summer",
        page_icon="🌞",
        layout="wide"
    )
    st.title('Welcome to the Hot Biel Summer App')
    st.markdown(
        """
        **Select a language below** and click on the welcome text to see more information about the project.
        Otherwise, feel free to explore each tab!
        _Note: Full translations, such as on charts, are not yet complete._
        """
    )

    # French
    st.markdown(
        """
        **Sélectionnez une langue ci-dessous** et cliquez sur le texte de bienvenue pour en savoir plus sur le projet.
        Sinon, explorez librement chaque onglet !
        _Remarque : Les traductions complètes, notamment sur les graphiques, ne sont pas encore terminées._
        """
    )

    # German
    st.markdown(
        """
        **Wählen Sie unten eine Sprache aus** und klicken Sie auf den Willkommens-Text, um mehr über das Projekt zu erfahren.
        Ansonsten können Sie die Registerkarten erkunden!
        _Hinweis: Die vollständige Übersetzung, z. B. bei Diagrammen, ist noch nicht abgeschlossen._
        """
    )
    langdict = get_lang_dict()
    with st.expander(langdict['welcome_md_t']):
        st.markdown(load_markdown(langdict['welcome_md']))
    m1, m2, m3 = st.columns(3)
    with m1:
        city = st.radio(langdict['city'], ['biel', 'bern'])
    with m2:
        period = st.radio(langdict['period'], langdict['period_choice'])
    with m3:
        basemap = st.radio(langdict['basemap'], langdict['map_choice'])
    st.info(langdict['date_info'])
    lu_path, f_path, u_path, tpath, spath = get_files(city, period)
    year = '23' if city == 'biel' else '22'
    sdtn_path = Path.cwd() / 'data' / city / f'summer{year}_sdtn.csv'

    # Create tabs

    tab_station_map, tab_tn_sd, tab_geo_map, tab_hourly_evolution, tab_fitnah_map,  = st.tabs(langdict['tabs'])

    # -------------------------------------------------------------------
    # 2) Hourly Data
    # -------------------------------------------------------------------
    with tab_station_map:
        uhi_city_index(u_path, basemap, langdict)

    with tab_tn_sd:
        tn_sd(sdtn_path, tpath, basemap, langdict)

    with tab_geo_map:
        tab_explore_geodata(lu_path, basemap, langdict)

    with tab_hourly_evolution:
        hourly_evolution(u_path, langdict)

    with tab_fitnah_map:
        fitnah_tab(f_path, basemap, langdict)


def uhi_city_index(uhi_path, basemap, langdict):
    st.subheader(langdict['uhi_title'])
    with st.expander(langdict['uhi_md_t']):
        st.markdown(load_markdown(langdict['uhi_md']))
    u1, u2 = st.columns(2)
    # Select Data Type (UHI or City Index)
    with u1:
        data_type = st.radio(langdict['dtype_uhi'], ['city_index', 'uhi'], key="data_type_selector")
    # Visualization mode selection
    with u2:
        hour = st.slider(langdict['Hour'], min_value=0, max_value=23, step=1, key="hour_selector")

    uhi_ci_data = pd.read_csv(uhi_path)
    selected_data = uhi_ci_data[uhi_ci_data['hour'] == hour]

    ucol1, ucol2 = st.columns([2, 1])
    with ucol1:
        st.markdown(f"##### Map of {data_type.capitalize()} at {hour}:00")
        plot_uhi_ci_map(selected_data, data_type, hour, basemap)
    with ucol2:
        st.markdown(f"##### Distribution of {data_type} at Hour {hour}:00")

        plot_uhi_ci_histogram(selected_data, data_type, hour, 30)

def tn_sd(sdtn_path, daily_stats_path, basemap, langdict):
    st.subheader(langdict['sdtn_title'])
    daily_data = pd.read_csv(daily_stats_path)
    sdtn_data = pd.read_csv(sdtn_path)
    sdtn_geo = daily_data.merge(sdtn_data[['Name', 'logger', 'x', 'y']], how='left', on='logger')
    with st.expander(langdict['sdtn_md_t']):
        st.markdown(load_markdown(langdict['sdtn_md']))

    s1, s2 = st.columns([2, 1])
    with s1:
        metric = st.radio(
            langdict['dtype_tnsd'],
            ["Summer Days (daily_max)", "Tropical Nights (daily_min)"]
        )

        if "Summer" in metric:
            threshold_label = "Summer Days Threshold (°C)"
            default_threshold = 30
            data_col = "daily_max"
        else:
            threshold_label = "Tropical Nights Threshold (°C)"
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
        tn_sd_histogram(summary, threshold)

def hourly_evolution(uhi_path, langdict):
    st.subheader(langdict['uhi_hour_title'])
    station_data = pd.read_csv(uhi_path)
    # 1) Let user choose 'uhi' or 'city_index'
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
        plot_uhi_ci_evolution(station_data, selected_loggers, data_type)
    else:
        st.info(langdict['uhi_warning'])

def fitnah_tab(fitnah_path, basemap, langdict):
    st.subheader(langdict['fitnah_title'])
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
        st.markdown(f'##### Map of *{dtype}* {aggregator.capitalize()} with buffer {buffer_size}')
        plot_fitnah_map(sel_fitnah_data, aggregator, basemap)
    with fcol2:
        st.markdown(f"##### Histogram of *{dtype}* {aggregator.capitalize()} with buffer {buffer_size}")

        plot_fitnah_histogram(sel_fitnah_data, aggregator, dtype, buffer_size)


def tab_explore_geodata(landuse_path, basemap, langdict):
    st.subheader(langdict['geo_title'])

    landuse = pd.read_csv(landuse_path)
    g1, g2 = st.columns(2)
    with g1:
        landuse_type = st.selectbox(langdict['dtype_landuse'], langdict['description_dict'].values())
    with g2:
        buffer = st.selectbox(langdict['buffer'], landuse['buffer'].unique(), key='geodata_buffer')
    st.write(landuse_type)
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
