##############################################################################################################
__author__ = "Juan P. Zaldivar & Enric Millan"
__version__ = "1.0.0"
##############################################################################################################


##############################################################################################################
# IMPORTS ################################################################################ IMPORTS ###########
##############################################################################################################
import pandas as pd
import streamlit as st
from Modules import visualizations as vis


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

    st.set_page_config(page_title='Visualization Project', page_icon=':bar_chart:', layout='wide')
    st.header('Vehicle Collisions Analysis in New York City')
    st.subheader('Data from summer months of 2018 and 2020')
    st.write('Designed by Juan Pablo Zaldivar and Enric Millán')
    st.header('')


    # ----- LOAD DATA -----
    merged = load_data('merged.csv', 'Data/')
    df = merged[['COLLISION_ID', 'LONGITUDE', 'LATITUDE', 'BOROUGH', 'ZIP CODE', 'VEHICLE TYPE CODE 1', 'TOTAL INJURED', 'TOTAL KILLED', 'CRASH DATE', 'HOUR', 'MONTH', 'WEEKDAY', 'icon']]

    # ----- DATA DASHBOARD -----


    # ----- DATA PREVIEW -----
    with st.expander("Data Preview"):
        st.dataframe(df.head())


if __name__ == '__main__':
    app()
