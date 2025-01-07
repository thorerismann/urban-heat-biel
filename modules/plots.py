import pandas as pd
import streamlit as st
import plotly.express as px

def geodata_histogram(
    sel_geo_data: pd.DataFrame,
    dtype: str,
    buffer: int,
    langdict: dict,
    bins: int = 20
) -> None:
    """
    Create and display a histogram of the specified aggregator's values using Plotly.

    Parameters
    ----------
    sel_geo_data : pd.DataFrame
        Filtered DataFrame containing the aggregator column.
    buffer : int
        The selected buffer chosen by the user.
    dtype : str
        The selected data type (e.g., 'fitnah_ss', 'fitnah_sv', 'fitnah_temp', 'dem') for title labeling.
    bins : int, optional
        Number of bins in the histogram, by default 20,
    langdict : dict
        Language dictionariy


    Returns
    -------
    None
        This function displays a Plotly histogram in Streamlit.
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




def tn_sd_histogram(station_summary, threshold, lang_dict):
    fig_hist = px.histogram(
        station_summary,
        x="exceed_count",
        nbins=20,
        title=lang_dict['exceedences_title'] + f'{threshold} °C)',
        labels={"exceed_count": lang_dict['sensor_count']},
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
        title="Histogram {dtype} {aggregator}, {buffer}m",
        labels={aggregator: aggregator.capitalize()},
        height=550,
        width=500
    )

    fig.update_layout(
        xaxis_title=f"{aggregator.capitalize()} Value",
        yaxis_title="Frequency",
        template="plotly_white",
    )

    st.plotly_chart(fig)