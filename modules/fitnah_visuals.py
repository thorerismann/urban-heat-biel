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
import pydeck as pdk
import plotly.express as px
import pandas as pd
from typing import Union


def _normalize(series: pd.Series, min_val: float = 0, max_val: float = 255) -> pd.Series:
    """
    Normalize values in a Pandas Series to a specified range.

    Parameters
    ----------
    series : pd.Series
        The numeric Series to normalize.
    min_val : float, optional
        The minimum value of the target range, by default 0.
    max_val : float, optional
        The maximum value of the target range, by default 255.

    Returns
    -------
    pd.Series
        A Series with values scaled to the [min_val, max_val] range.
        NaN values are filled with 0.
    """
    series_min = series.min()
    series_max = series.max()
    denom = series_max - series_min if series_max != series_min else 1e-9

    return (
        (series - series_min) / denom * (max_val - min_val) + min_val
    ).fillna(0)


def build_html_table(df: pd.DataFrame, val_col: str) -> str:
    """
    Build an HTML table of the given val_col for hours [0..23], arranged horizontally.

    Hours form the column headers, and their corresponding values form the row cells.
    Missing hours are labeled 'N/A'.

    Parameters
    ----------
    df : pd.DataFrame
        A subset of station data for a single logger or station name, with 'hour' and val_col.
    val_col : str
        The column name containing numeric values to display.

    Returns
    -------
    str
        An HTML string representing the table.
    """
    # Create a dict: hour -> value
    hour_map = df.set_index("hour")[val_col].to_dict()

    # Build HTML rows (two rows: hours, then values)
    hours_html = "<tr>" + "".join(
        f"<th style='border:1px solid #ccc; padding:2px; background:#eee;'>{h}</th>"
        for h in range(24)
    ) + "</tr>"

    values_html = "<tr>" + "".join(
        f"<td style='border:1px solid #ccc; padding:2px;'>"
        f"{round(hour_map[h],2) if h in hour_map else 'N/A'}</td>"
        for h in range(24)
    ) + "</tr>"

    table_html = (
        f"<table style='border-collapse:collapse; font-size:11px;'>"
        f"{hours_html}{values_html}"
        f"</table>"
    )
    return table_html

def build_html_table_double_column(full: pd.DataFrame, val_col: str) -> str:
    """
    Build a vertical HTML table with two columns showing Hour and val_col for hours 0-11 and 12-23.

    Each row corresponds to a pair of hours: one from 0-11 and the other from 12-23.

    Parameters
    ----------
    full : pd.DataFrame
        Full dataframe containing 'hour' and the column specified by val_col.
    val_col : str
        The column name containing numeric values to display.

    Returns
    -------
    str
        An HTML string representing the table with 12 rows and 2 columns.
    """
    rows = []
    # Loop through hours 0-11
    for h in range(12):
        # Retrieve value for hour h
        match1 = full.loc[full["hour"] == h, val_col]
        if not match1.empty:
            val1 = round(match1.iloc[0], 2)
        else:
            val1 = "N/A"

        # Retrieve value for hour h+12
        match2 = full.loc[full["hour"] == (h + 12), val_col]
        if not match2.empty:
            val2 = round(match2.iloc[0], 2)
        else:
            val2 = "N/A"

        # Create table row with two cells
        row_html = (
            f"<tr>"
            f"<td style='border:1px solid #ccc; padding:2px;'><b>Hour {h}</b>: {val1}</td>"
            f"<td style='border:1px solid #ccc; padding:2px;'><b>Hour {h + 12}</b>: {val2}</td>"
            f"</tr>"
        )
        rows.append(row_html)

    # Combine all rows into a single table
    table_html = (
        "<table style='border-collapse:collapse; font-size:11px;'>"
        + "".join(rows) +
        "</table>"
    )
    return table_html

def build_html_table_vertical(full: pd.DataFrame, val_col: str) -> str:
    """
    Build a vertical HTML table showing Hour and val_col in rows (Hour 0..23).
    Missing hours are labeled 'N/A'.

    Parameters
    ----------
    full: pd.DataFrame
        Full dataframe
    val_col : str
        The column name containing numeric values to display.

    Returns
    -------
    str
        An HTML string representing the table.
    """
    rows = []
    # For each hour 0..23, retrieve the value or 'N/A'
    for h in range(24):
        # Filter df for the station's row with this hour
        match = full.loc[full["hour"] == h, val_col]
        if not match.empty:
            val = round(match.iloc[0], 2)
        else:
            val = "N/A"

        row_html = (
            f"<tr>"
            f"<th style='border:1px solid #ccc; padding:2px; background:#eee;'>Hour {h}</th>"
            f"<td style='border:1px solid #ccc; padding:2px;'>{val}</td>"
            f"</tr>"
        )
        rows.append(row_html)

    table_html = (
            "<table style='border-collapse:collapse; font-size:11px;'>"
            + "".join(rows) +
            "</table>"
    )
    return table_html


def plot_fitnah_map(
    sel_fitnah_data: pd.DataFrame,
    aggregator: str,
) -> None:
    """
    Render a PyDeck chart for the selected Fitnah data with polygons colored by an aggregator value.
    Includes a color-scale legend at the bottom.

    Parameters
    ----------
    sel_fitnah_data : pd.DataFrame
        Filtered DataFrame containing geometry coordinates and aggregator columns.
        Must include columns: ['geometry_coords', aggregator, 'logger', 'lat', 'lon'].
    aggregator : str
        The name of the aggregator column to use (e.g., 'min', 'max', 'mean', 'count').

    Returns
    -------
    None
        This function displays the PyDeck chart and a color legend directly in the Streamlit interface.
    """
    # Normalize values for color
    sel_fitnah_data["normalized_color"] = _normalize(sel_fitnah_data[aggregator], 0, 255)

    # Configure polygon styling
    layer = pdk.Layer(
        "PolygonLayer",
        data=sel_fitnah_data,
        get_polygon="geometry_coords",
        get_fill_color="[normalized_color, 100, 200, 150]",  # RGBA
        get_line_color="[0, 0, 0, 200]",  # RGBA
        # No extrusion here; polygons remain flat
        extruded=False,
        pickable=True,
        auto_highlight=True,
    )

    # Tooltip configuration
    tooltip = {
        "html": (
            "<b>Logger:</b> {logger}<br>"
            "<b>Max:</b> {max}<br>"
            "<b>Min:</b> {min}<br>"
            "<b>Mean:</b> {mean}<br>"
            "<b>Count:</b> {count}<br>"
            f"<b>{aggregator.capitalize()} (Selected):</b> {{{aggregator}}}"
        ),
        "style": {
            "backgroundColor": "steelblue",
            "color": "white",
            "fontSize": "12px",
            "padding": "5px",
        },
    }

    # Compute center for initial view
    center_lat = sel_fitnah_data["lat"].mean()
    center_lon = sel_fitnah_data["lon"].mean()

    # Set the view state
    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=12,
        pitch=0,
    )

    # Render the deck
    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip,
        )
    )

    # Show a color-scale legend
    val_min = sel_fitnah_data[aggregator].min()
    val_max = sel_fitnah_data[aggregator].max()

    legend_html = f"""
    <div style="margin-top:10px; padding: 10px; background-color: #2551b0; 
         border: 1px solid #ccc; width: 250px; color:white; font-family: Arial, sans-serif;">
        <b>Legend - {aggregator.capitalize()}</b>
        <div style="height: 20px; margin: 5px 0;
                    background: linear-gradient(to right, rgb(0,100,150), rgb(255,100,150)); 
                    position: relative;">
          <!-- Show numeric min and max above the bar -->
          <p></p>
          <div style="position: absolute; left: 0; top: -20px; font-size: 12px;">
            <b>{np.round(val_min)}</b>
          </div>
          <div style="position: absolute; right: 0; top: -20px; font-size: 12px;">
            <b>{np.round(val_max,2)}</b>
          </div>
        </div>
    </div>
    """
    st.markdown(legend_html, unsafe_allow_html=True)


def plot_fitnah_histogram(
    sel_fitnah_data: pd.DataFrame,
    aggregator: str,
    dtype: str,
    buffer: int,
    bins: int = 20
) -> None:
    """
    Create and display a histogram of the specified aggregator's values using Plotly.

    Parameters
    ----------
    sel_fitnah_data : pd.DataFrame
        Filtered DataFrame containing the aggregator column.
    aggregator : str
        The name of the aggregator column to use in the histogram (e.g., 'min', 'max', 'mean', 'count').
    dtype : str
        The selected data type (e.g., 'fitnah_ss', 'fitnah_sv', 'fitnah_temp', 'dem') for title labeling.
    buffer: int
        The buffer chosen by user
    bins : int, optional
        Number of bins in the histogram, by default 20

    Returns
    -------
    None
        This function displays a Plotly histogram in Streamlit.
    """

    fig = px.histogram(
        sel_fitnah_data,
        x=aggregator,
        nbins=bins,
        title=f"Histogram of {dtype} {aggregator} with buffer {buffer}",
        labels={aggregator: f"{aggregator.capitalize()} Value"},
        height=550,
        width=500
    )

    fig.update_layout(
        xaxis_title=f"{aggregator.capitalize()} Value",
        yaxis_title="Frequency",
        template="plotly_white",
    )

    st.plotly_chart(fig)


def tab_summer_days_tropical_nights(data: pd.DataFrame, data_col: str, metric: str, threshold: int):
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

    # 4) Plot Map
    # Normalize exceed_count for color scale
    val_min = station_summary["exceed_count"].min()
    val_max = station_summary["exceed_count"].max()
    denom = val_max - val_min if val_max != val_min else 1e-9
    station_summary["color_val"] = (
        (station_summary["exceed_count"] - val_min) / denom * 255
    ).fillna(0)

    # Define PyDeck scatter layer
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=station_summary,
        get_position="[x, y]",
        get_fill_color="[color_val, 100, 200, 200]",
        get_line_color="[0, 0, 0]",
        get_radius=200,
        pickable=True,
        auto_highlight=True,
    )

    # Tooltip for map
    tooltip = {
        "html": (
            "<b>Logger:</b> {logger}<br>"
            "<b>Name:</b> {Name}<br>"
            f"<b>Days Above {threshold} °C:</b> {{exceed_count}}<br>"
            f"<b>Reference Days Above {reference_threshold} °C:</b> {{reference_count}}"
        ),
        "style": {
            "backgroundColor": "steelblue",
            "color": "white",
            "fontSize": "12px",
            "padding": "5px",
        },
    }

    # Compute map center
    center_lat = station_summary["y"].mean()
    center_lon = station_summary["x"].mean()

    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=12,
        pitch=0
    )

    c1, c2 = st.columns([2,1])
    with c1:
        st.markdown(f"##### Map of {metric} Exceedances (Threshold={threshold} °C)")
        st.pydeck_chart(
            pdk.Deck(
                layers=[scatter_layer],
                initial_view_state=view_state,
                tooltip=tooltip
            )
        )

        # 5) Display Color-Scale Legend
        legend_html = f"""
        <div style="margin-top:10px; padding: 10px; background-color: #2551b0; border: 1px solid #ccc; width: 250px;
                    font-family: Arial, sans-serif; color:white;">
            <b>Legend - Exceed Count</b>
            <p></p>
            <div style="height: 20px; margin: 5px 0;
                        background: linear-gradient(to right, rgb(0,100,150), rgb(255,100,150));
                        position: relative;">
                <div style="position: absolute; left: 0; top: -20px; font-size: 12px;">
                    <b>{val_min}</b>
                </div>
                <div style="position: absolute; right: 0; top: -20px; font-size: 12px;">
                    <b>{val_max}</b>
                </div>
            </div>
            <p style="margin: 0; font-size: 12px;">
                Color scale from min <b>{val_min}</b> to max <b>{val_max}</b>.
            </p>
        </div>
        """
        st.markdown(legend_html, unsafe_allow_html=True)

    # 3) Plot Histogram
    with c2:
        st.markdown(f"##### Histogram of Exceedances > {threshold} °C")
        fig_hist = px.histogram(
            station_summary,
            x="exceed_count",
            nbins=20,
            title=f"Distribution of Exceedances (Threshold={threshold} °C)",
            labels={"exceed_count": "Days Above Threshold"},
            height=600,
            width=500
        )
        fig_hist.update_layout(template="plotly_white")
        st.plotly_chart(fig_hist, use_container_width=True)

def plot_uhi_ci_map(
    station_data: pd.DataFrame,
    full_data: pd.DataFrame,
    value_column: str,
    hour: int,
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

    Returns
    -------
    None
        Displays a PyDeck chart in Streamlit and a color-scale legend below.
    """

    # 1) Build an HTML table for all 24 hours, per logger/Name
    # --------------------------------------------------------
    # grouped = station_data.groupby(["logger", "Name"], as_index=False)
    grouped_full = full_data.groupby(["logger", "Name"], as_index=False)
    hour_tables = []
    for (logger_id, station_name), group_df in grouped_full:
        table_html = build_html_table_double_column(group_df, value_column)
        hour_tables.append({
            "logger": logger_id,
            "Name": station_name,
            "hour_table": table_html
        })

    df_tables = pd.DataFrame(hour_tables)

    # Merge the HTML table into the original data
    station_data = station_data.merge(df_tables, on=["logger", "Name"], how="left")

    # 2) Filter to selected hour for the map display
    # ---------------------------------------------
    hour_data = station_data[station_data["hour"] == hour].copy()
    hour_data[value_column] = np.round(hour_data[value_column], 2)

    # 3) Normalize color
    # ------------------
    val_min = hour_data[value_column].min()
    val_max = hour_data[value_column].max()
    denom = val_max - val_min if val_max != val_min else 1e-9

    hour_data["normalized_color"] = (
        (hour_data[value_column] - val_min) / denom * 255
    ).fillna(0)

    # 4) Define the scatter layer
    # ---------------------------
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=hour_data,
        get_position="[x, y]",
        get_fill_color="[normalized_color, 100, 150, 200]",
        get_line_color="[0, 0, 0]",
        get_radius=200,  # smaller circles
        pickable=True,
        auto_highlight=True,
    )

    # 5) Tooltip with logger, name, selected hour’s value, & 24-hour table
    # --------------------------------------------------------------------
    tooltip = {
        "html": (
            "<b>Logger:</b> {logger}<br>"
            "<b>Name:</b> {Name}<br>"
            f"<b>{value_column.capitalize()} (Hour {hour}):</b> {{{value_column}}}<br>"
            "<b>All Hours:</b><br>{hour_table}"
        ),
        "style": {
            "backgroundColor": "steelblue",
            "color": "black",
            "fontSize": "12px",
            "padding": "5px",
        },
    }

    # 6) Compute map center
    # ---------------------
    center_lat = hour_data["y"].mean()
    center_lon = hour_data["x"].mean()

    # 7) View state
    # -------------
    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=12,
        pitch=0,
        min_zoom=7,
        max_zoom=15,
    )

    # 8) Render the map in Streamlit
    # ------------------------------
    st.pydeck_chart(
        pdk.Deck(
            layers=[scatter_layer],
            initial_view_state=view_state,
            tooltip=tooltip,
        )
    )

    # 9) Display a color-scale legend below the map
    # ---------------------------------------------
    legend_html = f"""
    <div style="margin-top:10px; padding: 10px; background-color: #2551b0; border: 1px solid #ccc; width: 250px;
                font-family: Arial, sans-serif; color:white;">
        <b>Legend - {value_column.capitalize()}</b>
        <div style="height: 20px; margin: 5px 0;
                    background: linear-gradient(to right, rgb(0,100,150), rgb(255,100,150));
                    position: relative;">
            <p></p>
            <div style="position: absolute; left: 0; top: -20px; font-size: 12px;">
                <b>{np.round(val_min,2)}</b>
            </div>
            <div style="position: absolute; right: 0; top: -20px; font-size: 12px;">
                <b>{np.round(val_max,2)}</b>
            </div>
        </div>

    </div>
    """
    st.markdown(legend_html, unsafe_allow_html=True)


def plot_uhi_ci_histogram(
    selected_data: pd.DataFrame,
    data_type: str,
    hour: int,
    bins: int = 20
) -> None:
    """
    Create and display a histogram of UHI or City Index values for a specified hour.

    Parameters
    ----------
    selected_data : pd.DataFrame
        Filtered DataFrame containing columns for 'hour' and the data_type (e.g., 'uhi' or 'city_index').
    data_type : str
        The data type to histogram, e.g., 'uhi' or 'city_index'.
    hour : int
        The hour of the day (0..23) to visualize.
    bins : int, optional
        Number of bins for the histogram, by default 20

    Returns
    -------
    None
        Displays a Plotly histogram in Streamlit.
    """
    fig = px.histogram(
        selected_data,
        x=data_type.lower(),
        nbins=bins,
        title=f"Histogram of {data_type.capitalize()} Values at Hour {hour}:00",
        labels={data_type.lower(): f"{data_type} Value"},
        height=600,
        width=500
    )

    fig.update_layout(
        xaxis_title=f"{data_type.capitalize()} Value",
        yaxis_title="Frequency",
        template="plotly_white",
    )
    st.plotly_chart(fig)


def plot_uhi_ci_evolution(
    station_data: pd.DataFrame,
    loggers: list,
    data_type: str
) -> None:
    """
    Plot the hourly evolution of UHI or City Index for selected loggers.

    Parameters
    ----------
    station_data : pd.DataFrame
        DataFrame containing columns 'logger', 'hour', and the specified data_type (e.g., 'uhi' or 'city_index').
    loggers : list
        A list of logger IDs to include in the plot.
    data_type : str
        The data column to plot (e.g., 'uhi' or 'city_index').

    Returns
    -------
    None
        Displays a Plotly line chart in the Streamlit interface.
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
        title=f"Hourly Evolution of {data_type.capitalize()} for Selected Loggers",
        markers=True,
        labels={
            "hour": "Hour of Day",
            data_type: f"{data_type.capitalize()} Value"
        },
        height=700
    )
    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig, use_container_width=True)
