"""
Module: fitnah_visuals
======================

Provides functionalities for visualizing Fitnah geospatial data, including:
- A PyDeck-based map with polygons colored by a chosen aggregator (e.g., min, max, mean, count).
- A PyDeck-based map for station-based UHI or City Index values (hourly data).
- A Plotly histogram function for aggregator-based data.
- A Plotly histogram function for station-based UHI/CI data.
"""

import numpy as np
import streamlit as st
import plotly.express as px
import pandas as pd
from .structure import sensor_labels, map_dict

def plot_fitnah_map(
    sel_data: pd.DataFrame,
    aggregator: str,
    maptype: str,
) -> None:
    """
    Render a PyDeck chart for the selected Fitnah data with polygons colored by an aggregator value.
    Includes a color-scale legend at the bottom.

    Parameters
    ----------
    sel_data : pd.DataFrame
        Filtered DataFrame containing geometry coordinates and aggregator columns.
        Must include columns: ['geometry_coords', aggregator, 'logger', 'lat', 'lon'].
    aggregator : str
        The name of the aggregator column to use (e.g., 'min', 'max', 'mean', 'count').
    maptype: str
        The name of the map to use

    Returns
    -------
    None
        This function displays the PyDeck chart and a color legend directly in the Streamlit interface.
    """
    # Normalize values for color
    if 'logger' in sel_data.columns:
        sel_data['name'] = sel_data['logger'].apply(lambda x: sensor_labels.get(x, f"Logger {x}"))
    else:
        sel_data['name'] = "Unknown"
    for col in ['mean', 'max', 'min']:
        sel_data[col] = np.round(sel_data[col], 2)

    fig = px.scatter_map(
        sel_data,
        lat="lat",
        lon="lon",
        hover_name="name",
        hover_data=['logger','mean','max','min','count'],
        color=aggregator,  # Assigns the column to the color scale
        zoom=13,
        height=500,
    )
    fig.update_traces(marker={'size': 25})

    final_fig = update_with_swisstopo(fig, maptype)

    st.plotly_chart(final_fig)

def sdtn_map(data: pd.DataFrame, data_col: str, metric: str, threshold: int, maptype: str):
    """
    Tab for visualizing Summer Days and Tropical Nights with interactive thresholds.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing:
          - 'x', 'y': Coordinates for the map.
          - 'logger': Unique station identifier.
          - 'Name': Station name.
          - 'daily_max', 'daily_min': Temperature metrics for calculation.
    data_col:
        column name of data to use for thresholding (daily max or daily min)
    metric:
        matric user (tn or sd)
    threshold:
        threshold to use for tn or sd calculation
    maptype:
        maptype to use in background
    """
    st.subheader("Summer Days & Tropical Nights")

    # 1) Metric and Threshold Selection

    # 2) Calculate Exceedances
    # Count days above the threshold for each logger
    data["exceed_count"] = (data[data_col] > threshold).astype(int)
    reference_threshold = 30 if "Summer" in metric else 20
    data["reference_count"] = (data[data_col] > reference_threshold).astype(int)

    # Group by logger for plotting
    station_summary = data.groupby(["logger", "Name", "x", "y"], as_index=False).agg(
        exceed_count=("exceed_count", "sum"),
        reference_count=("reference_count", "sum"),
    )
    fig = px.scatter_map(
        station_summary,
        lat="y",
        lon="x",
        hover_name="Name",
        hover_data=['logger', 'exceed_count', 'reference_count'],
        color='exceed_count',  # Assigns the column to the color scale
        zoom=13,
        height=500,
    )
    fig.update_traces(marker={'size': 25})

    final_fig = update_with_swisstopo(fig, maptype)

    st.plotly_chart(final_fig)
    return station_summary


def plot_uhi_ci_map(
    station_data: pd.DataFrame,
    value_column: str,
    hour: int,
    maptype: str,
) -> None:
    """
    Render a PyDeck map for UHI or City Index station data at a specific hour,
    with a hover tooltip (showing a 24-hour table) and a color-scale legend.

    Parameters
    ----------
    station_data : pd.DataFrame
        DataFrame containing station data with columns:
          - 'logger'
          - 'Name'
          - 'hour' (0..23)
          - 'x', 'y' (map coordinates)
          - The 'value_column' chosen, e.g. 'uhi' or 'city_index'
    value_column : str
        The column to visualize, e.g. 'uhi' or 'city_index'.
    full_data: pd.DataFrame
        For making the tooltip
    hour : int
        The specific hour (0..23) for the main display on the map.
    maptype: str
        The basemap for display

    Returns
    -------
    None
        Displays a PyDeck chart in Streamlit and a color-scale legend below.
        :param maptype:
    """

    # 1) Build an HTML table for all 24 hours, per logger/Name
    # --------------------------------------------------------
    # Merge the HTML table into the original data
    # 2) Filter to selected hour for the map display
    # ---------------------------------------------
    hour_data = station_data[station_data["hour"] == hour].copy()
    hour_data[value_column] = np.round(hour_data[value_column], 2)

    fig = px.scatter_map(
        hour_data,
        lat="y",
        lon="x",
        hover_name="Name",
        hover_data=['city_index', 'uhi'],
        color=value_column,  # Assigns the column to the color scale
        zoom=12,
        height=500,
    )
    fig.update_traces(marker={'size': 25})

    final_fig = update_with_swisstopo(fig, maptype)
    st.plotly_chart(final_fig)

def plot_geodata(df, selection, maptype, langdict):
    """Plot polygons from geometry_coords plus scatter circles at each [lon, lat].
    :param langdict:
    """
    st.write('starting plot')
    rename_map = {str(k): v for k, v in langdict['description_dict'].items()}
    newdf = df.rename(columns=rename_map).copy()

    if 'logger' in newdf.columns:
        newdf['name'] = newdf['logger'].apply(lambda x: sensor_labels.get(x, f"Logger {x}"))
    else:
        newdf['name'] = "Unknown"
    newdf['name_num'] = newdf['name'] + '_' + newdf['logger'].astype(str)
    fig = px.scatter_map(
        newdf,
        lat="lat",
        lon="lon",
        hover_name="name_num",
        hover_data=langdict['description_dict'].values(),
        color=selection,  # Assigns the column to the color scale
        zoom=12,
        height=500,
    )
    fig.update_traces(marker={'size': 50})
    final_fig = update_with_swisstopo(fig, maptype)
    st.plotly_chart(final_fig)


def update_with_swisstopo(fig, maptype):
    if (maptype == 'Carte nationale suisse en couleur') | (maptype == 'Schweizer Landeskarte Farbe') | (maptype == 'Swiss national map color'):
        mtype = map_dict['Swiss national map color']
    else:
        mtype = map_dict['Swiss national map gray']
    mapstring = f'https://wmts.geo.admin.ch/1.0.0/{mtype}/default/current/3857/'
    newfig = fig.update_layout(
        map_style="white-bg",
        map_layers=[
            {
                "below": "traces",
                "sourcetype": "raster",
                "sourceattribution": "© swisstopo",
                "opacity": 0.4,
                "source": [
                    mapstring + "{z}/{x}/{y}.jpeg"
                ]
            }
        ],
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return newfig