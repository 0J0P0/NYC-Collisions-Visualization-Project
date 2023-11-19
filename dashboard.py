####################################################################################################
__author__ = "Juan P. Zaldivar & Enric Millan"
__version__ = "1.0.0"
####################################################################################################

"""
This module contains the functions for the web app.

Functions:
----------

load_data(file: str, path: str = "./") -> pd.DataFrame
    This function loads the data from a csv file.

app()
    This function creates the web app.
"""


####################################################################################################
# IMPORTS ################################################################################ IMPORTS #
####################################################################################################
import pandas as pd
import streamlit as st
from Modules.visualizations import *


####################################################################################################
# FUNCTIONS ############################################################################ FUNCTIONS #
####################################################################################################
@st.cache_data
def load_data(file: str, path: str = "./") -> pd.DataFrame:
    return pd.read_csv(path + file)


def app():
    st.set_page_config(page_title="Visualization Project", page_icon=":bar_chart:", layout="wide")
    st.header("Vehicle Collisions Analysis in New York City")
    st.subheader("Data from summer months of 2018 and 2020")
    st.header("")

    # ----- LOAD DATA -----
    collisions = load_data("collisions_clean.csv", "Data/")
    weather = load_data("weather_clean.csv", "Data/")

    # ----- DATA DASHBOARD -----
    col1, col2 = st.columns([1, 1.8])
    with col1:
        c = plot_radial_chart(collisions[['VEHICLE TYPE CODE 1']])
        st.altair_chart(c, use_container_width=True)

    with col2:
        c = plot_line_chart(collisions[['BOROUGH', 'CRASH TIME INTERVAL']])
        st.altair_chart(c, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        c = plot_bar_chart(collisions[['CONTRIBUTING FACTOR VEHICLE 1', 'COLLISION_ID']])
        st.altair_chart(c, use_container_width=True)

    with col2:
        c = plot_hex_chart()
        st.altair_chart(c, use_container_width=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        c = plot_heatmap(collisions[['CRASH TIME INTERVAL', 'DAY NAME', 'YEAR']])
        st.altair_chart(c, use_container_width=True)

    with col2:
        c = plot_slope_chart(collisions[['YEAR', 'TYPE OF DAY']])
        st.altair_chart(c, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    comb_data = load_data('merged_data.csv', 'Data/')
    c1, c2, c3 = plot_scatterplots(comb_data)
    
    with col1:
        st.altair_chart(c1, use_container_width=True)
    with col2:
        st.altair_chart(c2, use_container_width=True)
    with col3:
        st.altair_chart(c3, use_container_width=True)

    # ----- DATA METRICS -----
    col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
    with col1:
        c = plot_cars(5, '2018')
        st.altair_chart(c, use_container_width=True)
    with col2:
        st.metric(label='Deaths 2018', value='177', delta='')
    with col3:
        st.metric(label='Injured 2018', value='44459', delta='')
    with col4:
        st.metric(label='Collisions 2018', value='79383', delta='')

    col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
    with col1:
        c = plot_cars(9, '2020')
        st.altair_chart(c, use_container_width=True)
    with col2:
        st.metric(label='Deaths 2020', value='228', delta='29%')
    with col3:
        st.metric(label='Injured 2020', value='34832', delta='-22%')
    with col4:
        st.metric(label='Collisions 2020', value='36357', delta='-54%')

    # ----- DATA PREVIEW -----
    with st.expander("Collisions Data Preview"):
        st.dataframe(collisions.head())
    with st.expander("Weather Data Preview"):
        st.dataframe(weather.head())



if __name__ == '__main__':
    app()
