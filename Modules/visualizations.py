import os
import pandas as pd
import altair as alt
import h3pandas as h3
import streamlit as st
import geopandas as gpd


dir = '../Data'

colores_hex = ['#a3ffd6', '#d69bf5', '#ff8080', '#80ff80', '#80bfff', '#ffff66', '#ffcc66', '#c9cba3', '#66cccc', '#ff66b3', '#ffb056', '#98c1d9', '#ffafcc']


@st.cache_data
def plot_radial_chart(df: pd.DataFrame) -> alt.Chart:
    """
    Creates a radial chart to show the number of collisions by vehicle type.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the collisions data.
    
    Returns
    -------
    alt.Chart
        Radial chart with the number of collisions by vehicle type.
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
                    legend=None),
                    # legend=alt.Legend(title="Vehicle Type",
                    #                     orient='left',
                    #                   labelFontSize=10)),
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
    Creates a line chart to show the number of collisions during the day by borough.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the collisions data.
    
    Returns
    -------
    alt.Chart
        Line chart with the number of collisions during the day by borough.
    """

    population = pd.DataFrame({
        'BOROUGH': ['BRONX', 'BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND'],
        'POPULATION_2018': [1438000000, 2601000000, 1632000000, 2299000000, 474101],
        'POPULATION_2020': [1427000000, 2577000000, 1629000000, 2271000000, 475596],
        'CAR OWNERSHIP': [0.40, 0.44, 0.22, 0.62, 0.83]
    })

    population['MEAN POPULATION'] = population[['POPULATION_2018', 'POPULATION_2020']].mean(axis=1)

    df.insert(0, 'COUNT', 1)
    df = df.groupby(['BOROUGH', 'CRASH TIME INTERVAL']).count().reset_index()
    df = df.merge(population[['BOROUGH', 'MEAN POPULATION', 'CAR OWNERSHIP']], on='BOROUGH', how='left')

    df['NORMALIZED COUNT'] = df['COUNT'] * df['CAR OWNERSHIP'] 

    c = alt.Chart(df).mark_line(
    tooltip=True,
    size=2
    ).encode(
        x=alt.X('CRASH TIME INTERVAL:N',
                title='Hour of the Day',
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('NORMALIZED COUNT:Q', title='Number of Collisions'),
        color=alt.Color('BOROUGH:N',
                        legend=alt.Legend(title='Borough',
                                          labelFontSize=10,
                                          orient='bottom'),
                        scale=alt.Scale(range=['#a3ffd6', '#d69bf5', '#ff8080', '#80ff80', '#80bfff']))
    )

    return c


@st.cache_data
def plot_hex_chart(df: pd.DataFrame) -> alt.Chart:
    """
    """

    file_path = "./Data/new-york-city-boroughs-ny_.geojson"

    nyc_map = gpd.read_file(file_path)
    nyc_map_hex = nyc_map.h3.polyfill_resample(8)
    nyc_map_hex = nyc_map_hex.reset_index()

    collisions_geo = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['LONGITUDE'], df['LATITUDE']))

    collisions_geo.crs = "EPSG:4326"
    nyc_map_hex.crs = "EPSG:4326"

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

    print(type(c1 + c2))
    return c1 + c2


@st.cache_data
def plot_heatmap(df: pd.DataFrame) -> alt.Chart:

    c1 = alt.Chart(df).mark_rect(
        tooltip=True
    ).encode(
        x=alt.X('CRASH TIME INTERVAL:N',
                title='Hour of the Day',
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('DAY NAME:N',
                sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                title='Day of the Week'),
        color=alt.Color('count():Q',
                        title='Number of Collisions',
                        scale=alt.Scale(range=['#f0fff1', '#5603ad'])),
        tooltip=['count()']
    ).properties(
        title='Number of Collisions by Hour of the Day and Day of the Week in 2018'
    )

    return c1


@st.cache_data
def plot_slope_chart(df: pd.DataFrame) -> alt.Chart:

    df = df.loc[:, ['YEAR', 'TYPE OF DAY']]
    df.insert(0, 'COUNT', 1)

    df = df.groupby(['YEAR', 'TYPE OF DAY']).count().reset_index()
    # divide count by 5 if it is a weekday
    df['COUNT'] = df.apply(lambda x: x['COUNT']/5 if x['TYPE OF DAY'] == 'Weekday' else x['COUNT']/2, axis=1)


    slope = alt.Chart(df).mark_line().encode(
        x=alt.X('YEAR:N', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('COUNT:Q', title='Collisions per Day'),
        color=alt.Color('TYPE OF DAY:N', legend=alt.Legend(title='Day Type'))
    )

    pts = alt.Chart(df).mark_point(
        filled=True,
        opacity=1
    ).encode(
        x=alt.X('YEAR:N', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('COUNT:Q', title='Collisions per Day'),
        color=alt.Color('WEEKDAY:N',
                        scale=alt.Scale(range=['#B3E9C7', '#8367C7']),
                        legend=None)
    )
    return alt.layer(slope, pts)


@st.cache_data
def plot_scatterplots(df: pd.DataFrame) -> alt.Chart:
    """
    Creates three scatterplots to compare the number of df with the weather conditions.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the merged data.
    
    Returns
    -------
    alt.Chart
        Scatterplot with the mean temperature and the number of df.
    alt.Chart
        Scatterplot with the precipitation and the number of df.
    alt.Chart
        Scatterplot with the wind speed and the number of df.
    """

    t1 = alt.Chart(df).mark_point(
        filled=True,
        size=100,
        opacity=0.5
    ).encode(
        x=alt.X('MEAN_TEMP:Q',
                title='Mean Temperature',
                scale=alt.Scale(domain=[10, 30])),
        y=alt.Y('COLLISION COUNT:Q', title='Number of Collisions'),
        color=alt.Color('year(DATE):N',
                        scale=alt.Scale(range=['#A7C9C7', '#8367C7']),
                        legend=None)
    )

    t2 = alt.Chart(df).mark_point(
        filled=True,
        size=100,
        opacity=0.5
    ).encode(
        x=alt.X('PRCP:Q', title='Precipitation'),
        y=alt.Y('COLLISION COUNT:Q', title=''),
        color=alt.Color('year(DATE):N',
                        scale=alt.Scale(range=['#A7C9C7', '#8367C7']),
                        legend=None)
    )

    t3 = alt.Chart(df).mark_point(
        filled=True,
        size=100,
        opacity=0.5
    ).encode(
        x=alt.X('AWND:Q',
                scale=alt.Scale(domain=[1, 6.5]),
                title='Wind Speed'),
        y=alt.Y('COLLISION COUNT:Q', title=''),
        color=alt.Color('year(DATE):N',
                        scale=alt.Scale(range=['#A7C9C7', '#8367C7']),
                        title='Year'),
    )

    return t1, t2, t3