import pandas as pd
import streamlit as st
from Modules.visualizations import *


@st.cache_data
def load_data(file: str, path: str = "./") -> pd.DataFrame:
    return pd.read_csv(path + file)


def app():
    st.set_page_config(page_title="Visualization Project", page_icon=":bar_chart:", layout="wide")
    st.title("Visualization Project")

    # # ----- SIDEBAR -----
    # with st.sidebar:
    #     st.header("About")
    #     st.info("This an interactive dashboard to analyze the collisions in New York City 🗽💥🚗")

    #     st.header("Data")
    #     st.info("Explain data information here.")

    # ----- LOAD DATA -----
    collisions = load_data("collisions_clean.csv", "Data/")
    weather = load_data("weather_clean.csv", "Data/")


    # ----- DATA DASHBOARD -----
    col1, col2, col3 = st.columns([1, 2, 1])


    with col1:
        c = plot_radial_chart(collisions[['VEHICLE TYPE CODE 1']])
        st.altair_chart(c, use_container_width=True)

    with col2:
        c = plot_line_chart(collisions[['BOROUGH', 'CRASH TIME INTERVAL']])
        st.altair_chart(c, use_container_width=True)

    # with col3:
    #     c = plot_hex_chart(collisions)
    #     st.altair_chart(c, use_container_width=True)

    col4, col5 = st.columns([3, 1])

    with col4:
        c = plot_heatmap(collisions[['CRASH TIME INTERVAL', 'DAY NAME', 'YEAR']])
        st.altair_chart(c, use_container_width=True)

    with col5:
        c = plot_slope_chart(collisions)
        st.altair_chart(c, use_container_width=True)

    col6, col7, col8 = st.columns(3)
    comb_data = load_data('merged_data.csv', 'Data/')
    c6, c7, c8 = plot_scatterplots(comb_data)
    
    with col6:
        st.altair_chart(c6, use_container_width=True)
    with col7:
        st.altair_chart(c7, use_container_width=True)
    with col8:
        st.altair_chart(c8, use_container_width=True)

    # ----- DATA PREVIEW -----

    with st.expander("Collisions Data Preview"):
        st.dataframe(collisions.head())
    with st.expander("Weather Data Preview"):
        st.dataframe(weather.head())



if __name__ == '__main__':
    app()
