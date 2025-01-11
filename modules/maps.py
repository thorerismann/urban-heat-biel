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
from .structure import sensor_labels

def plot_fitnah_map(
    sel_data: pd.DataFrame,
    aggregator: str,
    maptype: str,
) -> None:
    """
    Render a PyDeck map with selected Fitnah data and color polygons by aggregator values.

    Parameters:
    sel_data : pd.DataFrame
        Filtered DataFrame containing geometry coordinates and aggregator columns.
    aggregator : str
        The column for color scaling (e.g., 'mean', 'max').
    maptype : str
        Selected SwissTopo basemap.

    Returns:
    None
        Displays the map in Streamlit.
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

def sdtn_map(
    data: pd.DataFrame,
    data_col: str,
    metric: str,
    threshold: int,
    maptype: str,
) -> pd.DataFrame:
    """
    Visualize Summer Days and Tropical Nights with adjustable thresholds.

    Parameters:
    data : pd.DataFrame
        DataFrame with temperature data for analysis.
    data_col : str
        Column for thresholding ('daily_max' or 'daily_min').
    metric : str
        Selected metric (e.g., 'Summer Days', 'Tropical Nights').
    threshold : int
        Temperature threshold for filtering.
    maptype : str
        Selected SwissTopo basemap.

    Returns:
    pd.DataFrame
        Aggregated data for histogram plotting.
    """
    data["exceed_count"] = (data[data_col] > threshold).astype(int)
    reference_threshold = 30 if "Summer" in metric else 20
    data["reference_count"] = (data[data_col] > reference_threshold).astype(int)

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
    Render a PyDeck map for UHI or City Index data at a specific hour.

    Parameters:
    station_data : pd.DataFrame
        Station data with hourly values.
    value_column : str
        Data column for visualization (e.g., 'uhi', 'city_index').
    hour : int
        Hour for filtering data.
    maptype : str
        Selected SwissTopo basemap.

    Returns:
    None
        Displays the map in Streamlit.
    """
    hour_data = station_data[station_data["hour"] == hour].copy()
    hour_data[value_column] = np.round(hour_data[value_column], 2)

    fig = px.scatter_map(
        hour_data,
        lat="y",
        lon="x",
        hover_name="Name",
        hover_data=['city_index', 'uhi'],
        color=value_column,
        zoom=12,
        height=500,
    )
    fig.update_traces(marker={'size': 25})

    final_fig = update_with_swisstopo(fig, maptype)
    st.plotly_chart(final_fig)

def plot_geodata(
    df: pd.DataFrame,
    selection: str,
    maptype: str,
    langdict: dict,
) -> None:
    """
    Plot polygons and scatter points from geospatial data.

    Parameters:
    df : pd.DataFrame
        DataFrame with geospatial data.
    selection : str
        Column for color scaling.
    maptype : str
        Selected SwissTopo basemap.
    langdict : dict
        Language dictionary for localization.

    Returns:
    None
        Displays the map in Streamlit.
    """
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


def update_with_swisstopo(fig, maptype: str) -> "plotly.graph_objects.Figure":
    """
    Updates a Plotly map with SwissTopo layers based on the selected map type.

    Parameters:
    fig : plotly.graph_objects.Figure
        The base Plotly figure.
    maptype : str
        Selected SwissTopo basemap.

    Returns:
    plotly.graph_objects.Figure
        Updated figure with SwissTopo basemap applied.
    """
    if maptype in ['Carte nationale suisse en couleur', 'Schweizer Landeskarte Farbe', 'Swiss National Map Color']:
        mapstring = 'https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/{z}/{x}/{y}.jpeg'
    elif maptype == 'SwissAlti3D':
        mapstring = 'https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.swissalti3d-reliefschattierung/default/current/3857/{z}/{x}/{y}.png'
    elif maptype in ['Bodenbedeckung', 'Landcover', 'Couverture du sol']:
        mapstring = "https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.vec200-landcover/default/current/3857/{z}/{x}/{y}.png"

    else:
        mapstring = 'https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-grau/default/current/3857/{z}/{x}/{y}.jpeg'

    newfig = fig.update_layout(
        map_style="white-bg",
        map_layers=[
            {
                "below": "traces",
                "sourcetype": "raster",
                "sourceattribution": "© swisstopo",
                "opacity": 0.4,
                "source": [
                    mapstring
                ]
            }
        ],
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    return newfig