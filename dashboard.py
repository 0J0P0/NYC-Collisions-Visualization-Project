import pandas as pd
import streamlit as st
from Modules.visualizations import *


@st.cache_data
def load_data(file: str, path: str = "./") -> pd.DataFrame:
    return pd.read_csv(path + file)


def app():
    st.set_page_config(page_title="Visualization Project", page_icon=":bar_chart:", layout="wide")
    st.title("Visualization Project")

    # ----- SIDEBAR -----
    with st.sidebar:
        st.header("About")
        st.info("This an interactive dashboard to analyze the collisions in New York City 🗽💥🚗")

        st.header("Data")
        st.info("Explain data information here.")

    # ----- LOAD DATA -----
    collisions = load_data("collisions_clean.csv", "Data/")
    weather = load_data("weather_clean.csv", "Data/")


    # ----- DATA DASHBOARD -----
    col1, col2, col3 = st.columns(3)


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
        collisions['YEAR'] = collisions['CRASH DATE'].astype(str).str[:4]
        c = plot_heatmap(collisions[['CRASH TIME INTERVAL', 'DAY NAME', 'YEAR']])
        st.altair_chart(c, use_container_width=True)

    with col5:
        collisions['WEEKDAY'] = collisions['DAY NAME'].apply(lambda x: 'Weekday' if x in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else 'Weekend')
        c = plot_slope_chart(collisions)
        st.altair_chart(c, use_container_width=True)

   
    datafr = load_data('merged_data.csv', 'Data/')
    c = plot_scatterplots(datafr)
    st.altair_chart(c, use_container_width=True)

    # ----- DATA PREVIEW -----

    with st.expander("Collisions Data Preview"):
        st.dataframe(collisions.head())
    with st.expander("Weather Data Preview"):
        st.dataframe(weather.head())












if __name__ == '__main__':
    app()
