import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import pydeck as pdk
import ast  # To safely evaluate strings into Python objects
from modules.fitnah_visuals import *
from modules.structure import main_display, fitnah_explanation, uhi_explanation, sdtn_explanation


# -------------------------------------------------------------------
# 1) App Setup
# -------------------------------------------------------------------
def main():
    st.set_page_config(
        page_title="Hot Biel Summer",
        page_icon="🌞",
        layout="wide"
    )
    main_display()
    city = st.selectbox('Select a city:', ['biel', 'bern'])
    fitnah_path = Path.cwd() / 'data' / city / 'data_viz_fitnah.csv'

    year = '23' if city == 'biel' else '22'
    daily_stats_path = Path.cwd() / 'data' / city / f'summer{year}_temp_stats.csv'
    sdtn_path = Path.cwd() / 'data' / city / f'summer{year}_sdtn.csv'
    uhi_path = Path.cwd() / 'data' / city / f'summer{year}_hourly_uhi_ci.csv'
    mpath = Path.cwd() / 'meteo' / 'meteo.csv'

    # Create tabs

    tab_fitnah_map, tab_station_map, tab_tn_sd, tab_hourly_evolution = st.tabs(
        ["FITNAH Model Data", "Station Data UHI & City Index", "Station Data Tropical Nights & Summer Days", "Hourly Evolution of the UHI & City Index"]
    )

    # -------------------------------------------------------------------
    # 2) Hourly Data
    # -------------------------------------------------------------------
    with tab_fitnah_map:
        st.subheader("Fitnah Station Values")
        fitnah_explanation()
        # Read in the data for the selected city
        fitnah_data = pd.read_csv(fitnah_path)

        # Convert 'geometry_coords' from string to list
        fitnah_data['geometry_coords'] = fitnah_data['geometry_coords'].apply(ast.literal_eval)
        f1, f2, f3 = st.columns(3)
        with f1:
        # Let the user choose buffer size and data type
            buffer_size = st.selectbox('Select buffer size:', [10, 50, 100, 500])
        with f2:
            dtype = st.selectbox('Select data type:', ['fitnah_ss', 'fitnah_sv', 'fitnah_temp', 'dem'])
        with f3:
            aggregator = st.selectbox('Select geospatial aggregator for visualization:',
                                      ['min', 'max', 'mean', 'count'])
        # Filter the data
        sel_fitnah_data = fitnah_data[
            (fitnah_data['buffer'] == buffer_size) &
            (fitnah_data['dtype'] == dtype)
            ]

        fcol1, fcol2 = st.columns([2,1])
        with fcol1:
            st.markdown(f'##### Map of *{dtype}* {aggregator.capitalize()} with buffer {buffer_size}')
            plot_fitnah_map(sel_fitnah_data, aggregator)
        with fcol2:
            st.markdown(f"##### Histogram of *{dtype}* {aggregator.capitalize()} with buffer {buffer_size}")

            plot_fitnah_histogram(sel_fitnah_data, aggregator, dtype, buffer_size)

    # -------------------------------------------------------------------
    # 3) Daily Data
    # -------------------------------------------------------------------
    with tab_station_map:
        st.subheader("UHI and City Index Visualization")
        uhi_explanation()
        u1, u2 = st.columns(2)
        # Select Data Type (UHI or City Index)
        with u1:
            data_type = st.radio('Select Data Type:', ['city_index', 'uhi'], key="data_type_selector")
        # Visualization mode selection
        with u2:
            hour = st.slider("Select Hour (24-hour format):", min_value=0, max_value=23, step=1, key="hour_selector")

        uhi_ci_data = pd.read_csv(uhi_path)
        selected_data = uhi_ci_data[uhi_ci_data['hour'] == hour]

        ucol1, ucol2 = st.columns([2,1])
        with ucol1:
            st.markdown(f"##### Map of {data_type.capitalize()} at {hour}:00")
            plot_uhi_ci_map(selected_data, uhi_ci_data, data_type, hour)
        with ucol2:
            st.markdown(f"##### Distribution of {data_type} at Hour {hour}:00")

            plot_uhi_ci_histogram(selected_data, data_type, hour, 30)



    # -------------------------------------------------------------------
    # 4) Data Map
    # -------------------------------------------------------------------
    with tab_tn_sd:
        daily_data = pd.read_csv(daily_stats_path)
        sdtn_data = pd.read_csv(sdtn_path)
        sdtn_geo = daily_data.merge(sdtn_data[['Name','logger','x','y']], how='left', on='logger')
        sdtn_explanation()
        s1, s2 = st.columns([2,1])
        with s1:
            metric = st.radio(
                "Select Metric:",
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
        tab_summer_days_tropical_nights(sdtn_geo, data_col, metric, threshold)

    # -------------------------------------------------------------------
    # 5) Correlations
    # -------------------------------------------------------------------
    with tab_hourly_evolution:
        st.subheader("Select Loggers for UHI/CI Hourly Evolution")
        station_data = pd.read_csv(uhi_path)
        st.text(
            'Select stations to plot their average hourly UHI / City Index evolution over the course of the day for summer 2023.')

        # 1) Let user choose 'uhi' or 'city_index'
        h1, h2 = st.columns([1,2])
        with h1:
            data_type = st.radio("Select Data Type:", ["uhi", "city_index"], index=0)

        # 2) Multi-select for loggers
        with h2:
            selected_loggers = st.multiselect(
                "Select one or more loggers to plot:",
                options=sorted(station_data["logger"].unique()),
                default=[]
            )

        # 3) If user selects at least one logger, plot the line chart
        if selected_loggers:
            plot_uhi_ci_evolution(station_data, selected_loggers, data_type)
        else:
            st.info("Please select at least one logger to see the time evolution plot.")


# -------------------------------------------------------------------
# 6) Entry Point
# -------------------------------------------------------------------
if __name__ == "__main__":
    main()
