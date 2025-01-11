"""
Module: plots
================

This module provides visualization functions using Plotly for creating histograms,
line plots, and other interactive plots for geospatial and temporal data.

Functions:
- geodata_histogram
- plot_uhi_ci_evolution
- plot_uhi_ci_histogram
- tn_sd_histogram
- plot_fitnah_histogram
"""


import pandas as pd
import streamlit as st
import plotly.express as px

def geodata_histogram(
    sel_geo_data: pd.DataFrame,
    dtype: str,
    buffer: int,
    langdict: dict,
    bins: int = 20,
) -> None:
    """
    Create and display a histogram of geospatial data within a specified buffer.

    Parameters:
    sel_geo_data : pd.DataFrame
        Filtered DataFrame containing geospatial data.
    dtype : str
        Data type for the histogram (e.g., 'fitnah_ss', 'fitnah_sv').
    buffer : int
        The buffer distance in meters.
    langdict : dict
        Language dictionary for localization.
    bins : int, optional
        Number of bins for the histogram (default: 20).

    Returns:
    None
        Displays the histogram in Streamlit.
    """

    refdict = {v:str(k) for k,v in langdict['description_dict'].items()}
    fig = px.histogram(
        sel_geo_data,
        x=refdict[dtype],
        nbins=bins,
        title=f"Histogram of the count of {dtype} raster cells within a {buffer} meter buffer.",
        height=550,
        width=500
    )

    fig.update_layout(
        xaxis_title=f"Number of {dtype} raster cells",
        yaxis_title="Sensor Count",
        template="plotly_white",
    )

    st.plotly_chart(fig)

def plot_uhi_ci_evolution(
    station_data: pd.DataFrame,
    loggers: list,
    data_type: str,
    lang_dict: dict
) -> None:
    """
    Plot the hourly evolution of UHI or City Index for selected loggers.

    Parameters:
    station_data : pd.DataFrame
        DataFrame containing columns for 'logger', 'hour', and data values.
    loggers : list
        List of logger IDs to include in the plot.
    data_type : str
        Data column to plot (e.g., 'uhi', 'city_index').
    lang_dict : dict
        Language dictionary for translations


    Returns:
    None
        Displays a line chart in Streamlit.
        :param lang_dict:
    """

    # Filter data for the selected loggers
    subset = station_data[station_data["logger"].isin(loggers)].copy()
    if subset.empty:
        st.warning("No data found for the selected logger(s).")
        return

    # Optionally sort by hour for a cleaner line
    subset.sort_values("hour", inplace=True)

    # Create a line chart
    fig = px.line(
        subset,
        x="hour",
        y=data_type,  # e.g., "uhi" or "city_index"
        color="logger",
        title=lang_dict['hourly_evol_title'] + f' {data_type.capitalize()} ',
        markers=True,
        labels={
            "hour": lang_dict['Hour'],
            data_type: f"{data_type.capitalize()}"
        },
        height=700
    )
    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True)


def plot_uhi_ci_histogram(
    selected_data: pd.DataFrame,
    data_type: str,
    hour_str: str,
    lang_dict: dict,
    bins: int = 20,
) -> None:
    """
    Create and display a histogram of UHI or City Index values at a specified hour.

    Parameters:
    selected_data : pd.DataFrame
        Filtered DataFrame with hourly UHI or City Index data.
    data_type : str
        Data type for the histogram (e.g., 'uhi', 'city_index').
    hour : int
        Hour of the day to filter data.
    lang_dict : dict
        Language dictionary for translations
    bins : int, optional
        Number of bins for the histogram (default: 20).

    Returns:
    None
        Displays the histogram in Streamlit.
        :param hour_str:
    """

    fig = px.histogram(
        selected_data,
        x=data_type.lower(),
        nbins=bins,
        title=f"{data_type.capitalize()} - {hour_str}:00",
        labels={data_type.lower(): f"{data_type}"},
        height=600,
        width=500
    )

    fig.update_layout(
        xaxis_title=f"{data_type.capitalize()}",
        yaxis_title=lang_dict['frequency'],
        template="plotly_white",
    )
    st.plotly_chart(fig)




def tn_sd_histogram(
    station_summary: pd.DataFrame,
    threshold: int,
    lang_dict: dict,
) -> None:
    """
    Create and display a histogram for Summer Days or Tropical Nights threshold exceedances.

    Parameters:
    station_summary : pd.DataFrame
        DataFrame summarizing exceedances per station.
    threshold : int
        Temperature threshold used for exceedance calculations.
    lang_dict : dict
        Language dictionary for localization.

    Returns:
    None
        Displays the histogram in Streamlit.
    """

    fig_hist = px.histogram(
        station_summary,
        x="exceed_count",
        nbins=20,
        title=lang_dict['exceedences_title'] + f'{threshold} °C)',
        labels={"exceed_count": lang_dict['frequency']},
        height=600,
        width=500
    )
    fig_hist.update_layout(template="plotly_white")
    st.plotly_chart(fig_hist, use_container_width=True)

def plot_fitnah_histogram(
    sel_fitnah_data: pd.DataFrame,
    aggregator: str,
    dtype: str,
    buffer: int,
    lang_dict: dict,
    bins: int = 20,
) -> None:
    """
    Create and display a histogram for Fitnah data using a specified aggregator.

    Parameters:
    sel_fitnah_data : pd.DataFrame
        Filtered DataFrame with aggregated Fitnah data.
    aggregator : str
        Aggregator column for histogram values (e.g., 'min', 'max', 'mean').
    dtype : str
        Data type for the histogram (e.g., 'fitnah_ss', 'fitnah_sv').
    buffer : int
        Buffer distance in meters.
    lang_dict: dict
        Language dictionary for translations
    bins : int, optional
        Number of bins for the histogram (default: 20).

    Returns:
    None
        Displays the histogram in Streamlit.
    """


    fig = px.histogram(
        sel_fitnah_data,
        x=aggregator,
        nbins=bins,
        title=f"{dtype} - {aggregator} - {buffer}m",
        labels={aggregator: aggregator.capitalize()},
        height=550,
        width=500
    )

    fig.update_layout(
        xaxis_title=f"{aggregator.capitalize()}",
        yaxis_title=lang_dict['frequency'],
        template="plotly_white",
    )

    st.plotly_chart(fig)