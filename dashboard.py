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
    col1, col2, col3 = st.columns([1, 7, 1])
    with col1:
        st.metric(label='Deaths 2020', value='228', delta='129%')

    with col2:
        # c = plot_cars()
        # st.altair_chart(c, use_container_width=True)
        st.empty()

    with col3:
        st.metric(label='Injured 2020', value='34832', delta="-78%")

    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        c = plot_radial_chart(collisions[['VEHICLE TYPE CODE 1']])
        st.altair_chart(c, use_container_width=True)

    with col2:
        c = plot_line_chart(collisions[['BOROUGH', 'CRASH TIME INTERVAL']])
        st.altair_chart(c, use_container_width=True)

    with col3:
        c = plot_hex_chart(collisions)
        st.altair_chart(c, use_container_width=True)

    # col1, col2 = st.columns([1, 2])
    # with col2:
    #     c = plot_radial_chart(collisions[['VEHICLE TYPE CODE 1']])
    #     st.altair_chart(c, use_container_width=True)

    # with col2:
    #     c = plot_lollipop_chart(collisions[['VEHICLE TYPE CODE 1']])

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


    # ----- DATA PREVIEW -----
    with st.expander("Collisions Data Preview"):
        st.dataframe(collisions.head())
    with st.expander("Weather Data Preview"):
        st.dataframe(weather.head())



if __name__ == '__main__':
    app()
