##############################################################################################################
__author__ = "Juan P. Zaldivar & Enric Millan"
__version__ = "1.0.0"
##############################################################################################################


##############################################################################################################
# IMPORTS ################################################################################ IMPORTS ###########
##############################################################################################################
import pandas as pd
import altair as alt
import streamlit as st
from Modules import final_visualization as vi


##############################################################################################################
# FUNCTIONS ############################################################################ FUNCTIONS ###########
##############################################################################################################
@st.cache_data
def load_data(file: str, path: str = './') -> pd.DataFrame:
    return pd.read_csv(path + file)


def app():
    """
    .
    """

    st.set_page_config(page_title='Visualization Project', page_icon=':bar_chart:', layout='centered')
    st.header('Vehicle Collisions Analysis in New York City')
    st.subheader('Data from summer months of 2018')
    st.write('Designed by Juan Pablo Zaldivar and Enric Millán')
    st.header('')


    # ----- LOAD DATA -----
    merged = load_data('merged.csv', 'Data/')
    df = merged[['COLLISION_ID', 'LONGITUDE', 'LATITUDE', 'BOROUGH', 'ZIP CODE', 'VEHICLE TYPE CODE 1', 'TOTAL INJURED', 'TOTAL KILLED', 'CRASH DATE', 'HOUR', 'MONTH', 'WEEKDAY', 'icon']]


    # ----- DATA DASHBOARD -----
    hour_line = vi.hour_line_chart(df)

    day_line = vi.day_line_chart(df)

    dot_map = vi.dotmap_chart(df)

    bars = vi.bar_chart(df)

    kpi1 = vi.kpi_collisions(df, 'Collisions Count')
    kpi2, kpi3 = vi.kpi_persons(df, 'Injured Sum', 'Killed Sum')

    legends, boroughs_legends = vi.legend_chart(df)

    final = alt.vconcat(alt.vconcat(legends, alt.hconcat(alt.vconcat(dot_map, boroughs_legends, hour_line).resolve_scale(color='independent'), alt.vconcat(alt.hconcat(kpi1, kpi2, kpi3), alt.vconcat(day_line, bars).resolve_scale(color='independent')))))  
    
    st.altair_chart(final, use_container_width=True)


    # ----- DATA PREVIEW -----
    with st.expander("Data Preview"):
        st.dataframe(df.head())


if __name__ == '__main__':
    app()


    # st.altair_chart(legends, use_container_width=True)

    # c1, c2 = st.columns([1, 3])
    # with c1:
    #     st.altair_chart(dot_map, use_container_width=True)
    # with c2:
    #     r1, r2 = st.container(), st.container()
    #     with r1:
    #         c3, c4, c5 = st.columns(3)
    #         with c3:
    #             st.altair_chart(kpi1, use_container_width=True)
    #         with c4:
    #             st.altair_chart(kpi2, use_container_width=True)
    #         with c5:
    #             st.altair_chart(kpi3, use_container_width=True)
    #     with r2:
    #         st.altair_chart(day_line, use_container_width=True)

    # c3, c4 = st.columns(2)
    # with c3:
    #     st.altair_chart(hour_line, use_container_width=True)
    # with c4:
    #     st.altair_chart(bars, use_container_width=True)

    # st.altair_chart(temp, use_container_width=True)