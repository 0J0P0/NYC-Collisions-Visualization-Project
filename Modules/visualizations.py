import pandas as pd
import altair as alt
import streamlit as st
import geopandas as gpd


dir = '../Data'

colores_hex = ['#a3ffd6', '#d69bf5', '#ff8080', '#80ff80', '#80bfff', '#ffff66', '#ffcc66', '#c9cba3', '#66cccc', '#ff66b3', '#ffb056', '#98c1d9', '#ffafcc']


@st.cache_data
def plot_radial_chart(df: pd.DataFrame) -> alt.Chart:
    """
    """

    c = alt.Chart(df).encode(
    alt.Theta("VEHICLE TYPE CODE 1:N",
              stack = True,
              sort=alt.EncodingSortField(field="count", op="count", order='descending')),
    alt.Radius("count()",
               scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
    color=alt.Color("VEHICLE TYPE CODE 1:N",
                    sort=alt.EncodingSortField(field="count", op="count", order='descending'),
                    scale=alt.Scale(range=colores_hex),
                    legend=alt.Legend(title="Vehicle Type")),
    ).mark_arc(
        innerRadius=5, stroke="#fff"
    )

    text = c.mark_text(
        align='center',
        baseline='middle',
        radiusOffset=20,
        fontSize=12.5,
    ).encode(
        text='count()'
    )

    return c + text


@st.cache_data
def plot_line_chart(df: pd.DataFrame) -> alt.Chart:
    """
    """

    population = pd.DataFrame({
        'BOROUGH': ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND'],
        'POPULATION_2018': [1438000000, 2601000000, 1632000000, 2299000000, 474101],
        'POPULATION_2020': [1427000000, 2577000000, 1629000000, 2271000000, 475596],
        'CAR OWNERSHIP': [0.40, 0.44, 0.22, 0.62, 0.83]
    })

    population['MEAN POPULATION'] = population[['POPULATION_2018', 'POPULATION_2020']].mean(axis=1)

    df = df[['BOROUGH', 'CRASH TIME INTERVAL']]
    df.insert(0, 'COUNT', 1)

    df = df.groupby(['BOROUGH', 'CRASH TIME INTERVAL']).count().reset_index()
    df = df.merge(population[['BOROUGH', 'MEAN POPULATION', 'CAR OWNERSHIP']], on='BOROUGH', how='left')

    df['NORMALIZED COUNT'] = df['COUNT'] * df['CAR OWNERSHIP'] 

    c = alt.Chart(df).mark_line(
    tooltip=True,
    size=2
    ).encode(
        x=alt.X('CRASH TIME INTERVAL:N',
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('NORMALIZED COUNT:Q'),
        color=alt.Color('BOROUGH:N',
                        legend=alt.Legend(title="Borough",
                                          orient='bottom'),
                        scale=alt.Scale(range=['#a3ffd6', '#d69bf5', '#ff8080', '#80ff80', '#80bfff']))
    )

    return c


@st.cache_data
def plot_hex_chart(df: pd.DataFrame) -> alt.Chart:
    """
    """

    nyc_map = gpd.read_file(f'{dir}/new-york-city-boroughs-ny_.geojson')
    nyc_map_hex = nyc_map.h3.polyfill_resample(8)
    nyc_map_hex = nyc_map_hex.reset_index()

    collisions_geo = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['LONGITUDE'], df['LATITUDE']))

    df = collisions_geo.sjoin(nyc_map_hex, how='right')

    tmp = df.groupby(['h3_polyfill', 'name']).count().reset_index()
    tmp = tmp[['h3_polyfill', 'name', 'COLLISION_ID']]


    tmp.columns = ['h3_polyfill', 'name', 'count']

    df = df.merge(tmp, on=['h3_polyfill', 'name'], how='left')

    df = df[['h3_polyfill', 'name', 'count', 'geometry']]

    df = df.drop_duplicates(subset=['h3_polyfill', 'name'])

    c1 = alt.Chart(df).mark_geoshape(
        stroke='white',
        strokeWidth=1,
        filled=True
    ).encode(
        color=alt.Color('count:Q',
                        scale=alt.Scale(range=['#B3E9C7', '#5603ad']),
                        title='Borough'),
    ).project(
        type='identity', reflectY=True
    )

    c2 = alt.Chart(nyc_map).mark_geoshape(
        stroke='#1d3557',
        strokeWidth=1,
        opacity=0.6,
        filled=False
    ).project(
        type='identity', reflectY=True
    )

    return c1 + c2