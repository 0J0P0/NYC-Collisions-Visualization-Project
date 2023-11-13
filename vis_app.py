import streamlit as st
import pandas as pd
import altair as alt


@st.cache_data
def plot_violin(data: pd.DataFrame) -> alt.Chart:
    return alt.Chart(data[['COLLISION_ID', 'CRASH TIME INTERVAL', 'CRASH DATE']]).transform_timeunit(
      timeUnit='year',
      field='CRASH DATE',
      as_='YEAR'
    ).transform_density(
        'CRASH TIME INTERVAL',
        as_=['CRASH TIME INTERVAL', 'density'],
        extent=[0, 23],
        groupby=['YEAR']
    ).mark_area(orient='horizontal').encode(
        alt.X('density:Q',
            stack='center',
            impute=None,
            title=None,
            axis=alt.Axis(labels=False, values=[0], grid=False, ticks=True)),
        alt.Y('CRASH TIME INTERVAL:Q',
            title='Hour of the Day',
            axis=alt.Axis(labelAngle=0)),
        alt.Color('YEAR:O',
                scale=alt.Scale(domain=['2018', '2020'], range=['lightblue', 'lightgreen']),
                legend=None),
        alt.Column('YEAR:O',
                    header=alt.Header(titleOrient='bottom', labelOrient='bottom', labelPadding=0),
                    spacing=0,
                    title=None)
    ).configure_view(
        stroke=None
    )

@st.cache_data
def plot_bars(data: pd.DataFrame) -> alt.Chart:
    return alt.Chart(data).mark_bar().encode(
        x=alt.X('count():Q', title='Number of Collisions'),
        y=alt.Y('DAY NAME:O', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], title='Day of the Week'),
        color=alt.Color('DAY NAME:O', scale=alt.Scale(domain=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], range=['lightgray', 'lightgray', 'lightgray', 'lightgray', 'lightgray', '#fcef00', '#fcef00']), legend=None)
    ).properties(
        title='Number of Collisions by Day of the Week'
    )


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
    col1, col2 = st.columns(2)

    with col1:
        st.altair_chart(plot_bars(collisions), use_container_width=True)

    with col2:
        st.altair_chart(plot_violin(collisions), use_container_width=True)  

    # ----- DATA PREVIEW -----
    with st.expander("Collisions Data Preview"):
        st.dataframe(collisions.head())
    with st.expander("Weather Data Preview"):
        st.dataframe(weather.head())












if __name__ == '__main__':
    app()
