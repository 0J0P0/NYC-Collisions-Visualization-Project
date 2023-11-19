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
                        sort=alt.EncodingSortField(field="count",
                                                op="count",
                                                order='descending'),
                        scale=alt.Scale(range=colores_hex),
                        legend=alt.Legend(title="Vehicle Type",
                                        orient='left',
                                        labelFontSize=10))
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

    return alt.layer(c + text).properties(title='Collisions by Vehicle Type')


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
                                          labelFontSize=12,
                                          orient='bottom'),
                        scale=alt.Scale(range=['#a3ffd6', '#d69bf5', '#ff8080', '#80ff80', '#80bfff'])),
        tooltip=['BOROUGH', 'CRASH TIME INTERVAL', 'COUNT']
    ).properties(
        title='Collisions by Hour of the Day'
    )

    return c


@st.cache_data
def plot_hex_chart() -> alt.Chart:
    """
    Creates a hexagonal map chart to show the number of collisions by borough.

    Returns
    -------
    alt.Chart
        Hexagonal map chart with the number of collisions by borough.
    """

    hex_url = 'https://raw.githubusercontent.com/0J0P0/Visualization-Project/main/Data/new-york-city-boroughs-ny_hex.geojson'
    df = alt.Data(url=hex_url, format=alt.DataFormat(property="features"))

    c1 = alt.Chart(df).mark_geoshape(
        stroke='white',
        strokeWidth=1,
        filled=True,
        tooltip=True
    ).encode(
        color=alt.Color('properties.count:Q',
                        scale=alt.Scale(range=['#B3E9C7', '#5603ad']),
                        legend=alt.Legend(title='Collisions',
                                          labelFontSize=10,
                                          orient='right')),
    ).project(
        type='identity', reflectY=True
    ).properties(
        title='Collisions by Borough'
    )

    map_url = 'https://raw.githubusercontent.com/0J0P0/Visualization-Project/main/Data/new-york-city-boroughs-ny_.geojson'
    borders = alt.Data(url=map_url, format=alt.DataFormat(property="features"))
    
    c2 = alt.Chart(borders).mark_geoshape(
        stroke='#8367C7',
        strokeWidth=2,
        opacity=0.6,
        filled=False,
        tooltip=False
    ).project(
        type='identity', reflectY=True
    )

    # c3 = alt.Chart(borders).mark_text(
    #     align='center',
    #     baseline='middle',
    #     fontSize=12,
    #     fontWeight='bold',
    #     dy=-10
    # ).encode(
    #     longitude='properties.longitude:Q',
    #     latitude='properties.latitude:Q',
    #     text='properties.borough:N'
    # ).project(
    #     type='identity', reflectY=True
    # )

    return (c1 + c2)


@st.cache_data
def plot_bar_chart(df: pd.DataFrame) -> alt.Chart:
    """
    Creates a bar chart to show the number of collisions by contributing factor.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the collisions data.
    
    Returns
    -------
    alt.Chart
        Bar chart with the number of collisions by contributing factor.
    """

    df = df.groupby('CONTRIBUTING FACTOR VEHICLE 1').count().reset_index()
    df = df.sort_values(by='COLLISION_ID', ascending=False)

    df = df[df['CONTRIBUTING FACTOR VEHICLE 1'] != 'Unspecified']
    df.columns = ['CONTRIBUTING FACTOR VEHICLE 1', 'COUNT']
    df = df.head(5)

    c = alt.Chart(df).mark_bar(
        tooltip=True
    ).encode(
        x=alt.X('CONTRIBUTING FACTOR VEHICLE 1:N',
                title='Contributing Factor',
                sort=alt.EncodingSortField(field="COUNT", order="descending"),
                axis=alt.Axis(labelAngle=-30)),
        y=alt.Y('COUNT:Q',
                title='Number of Collisions'),
        tooltip=['CONTRIBUTING FACTOR VEHICLE 1:N', 'COUNT:Q']
    ).properties(
        title='Collisions by Contributing Factor'
    ).configure_mark(
        color='#8367C7'
    )

    return c


@st.cache_data
def plot_heatmap(df: pd.DataFrame) -> alt.Chart:
    """
    Creates a heatmap to show the number of collisions by hour of the day and day of the week.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the collisions data.
    
    Returns
    -------
    alt.Chart
        Heatmap with the number of collisions by hour of the day and day of the week.
    """

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
                        legend=alt.Legend(title='Collisions',
                                            labelFontSize=12),
                        scale=alt.Scale(domain=[100, 1400],
                                        range=['#f0fff1', '#5603ad'])),
        tooltip=['DAY NAME', 'CRASH TIME INTERVAL', 'count()']
    ).properties(
        height=300,
        title='Collisions by Hour of the Day and Day of the Week'
    )

    return c1


@st.cache_data
def plot_slope_chart(df: pd.DataFrame) -> alt.Chart:
    """
    Creates a slope chart to show the number of collisions by day type.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the collisions data.
    
    Returns
    -------
    alt.Chart
        Slope chart with the number of collisions by day type.
    """

    df.insert(0, 'COUNT', 1)
    df = df.groupby(['YEAR', 'TYPE OF DAY']).count().reset_index()
    df['COUNT'] = df.apply(lambda x: x['COUNT']/5 if x['TYPE OF DAY'] == 'Weekday' else x['COUNT']/2, axis=1)

    slope = alt.Chart(df).mark_line().encode(
        x=alt.X('YEAR:N', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('COUNT:Q', title='Collisions'),
        color=alt.Color('TYPE OF DAY:N', legend=alt.Legend(title='Day Type', labelFontSize=11))
    )

    pts = alt.Chart(df).mark_point(
        filled=True,
        opacity=1
    ).encode(
        x=alt.X('YEAR:N', title='', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('COUNT:Q', title=''),
        color=alt.Color('TYPE OF DAY:N',
                        scale=alt.Scale(range=['#B3E9C7', '#8367C7']),
                        legend=None)
    )
    return alt.layer(slope, pts).properties(height=300, title='Collisions by Day Type')


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
        y=alt.Y('COLLISION COUNT:Q', title='Collisions'),
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
        y=alt.Y('COLLISION COUNT:Q', title='',
                axis=alt.Axis(labels=False, ticks=False)),
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
        y=alt.Y('COLLISION COUNT:Q', title='',
                axis=alt.Axis(labels=False, ticks=False)),
        color=alt.Color('year(DATE):N',
                        scale=alt.Scale(range=['#A7C9C7', '#8367C7']),
                        legend=alt.Legend(title='Year', labelFontSize=11))
    )

    return t1, t2, t3


@st.cache_data
def plot_cars(idx: int, year: str):
    """
    Creates a row of cars to show the number of collisions with injured people.

    Parameters
    ----------
    idx : int
        Number of collisions with injured people.
    year : str
        Year of the data.
    
    Returns
    -------
    alt.Chart
        Row of cars to show the number of collisions with injured people.
    """

    car = ("M640 320V368C640 385.7 625.7 400 608 400H574.7C567.1 445.4 527.6 480 480 480C432.4 480 392.9 445.4 385.3 400H254.7C247.1 445.4 207.6 480 160 480C112.4 480 72.94 445.4 65.33 400H32C14.33 400 0 385.7 0 368V256C0 228.9 16.81 205.8 40.56 196.4L82.2 92.35C96.78 55.9 132.1 32 171.3 32H353.2C382.4 32 409.1 45.26 428.2 68.03L528.2 193C591.2 200.1 640 254.8 640 319.1V320zM171.3 96C158.2 96 146.5 103.1 141.6 116.1L111.3 192H224V96H171.3zM272 192H445.4L378.2 108C372.2 100.4 362.1 96 353.2 96H272V192zM525.3 400C527 394.1 528 389.6 528 384C528 357.5 506.5 336 480 336C453.5 336 432 357.5 432 384C432 389.6 432.1 394.1 434.7 400C441.3 418.6 459.1 432 480 432C500.9 432 518.7 418.6 525.3 400zM205.3 400C207 394.1 208 389.6 208 384C208 357.5 186.5 336 160 336C133.5 336 112 357.5 112 384C112 389.6 112.1 394.1 114.7 400C121.3 418.6 139.1 432 160 432C180.9 432 198.7 418.6 205.3 400z"
    )

    data = pd.DataFrame([dict(id=i) for i in range(1, 11)])
    data['color'] = ['kill/injured' if i <= idx else 'non' for i in range(1, 11)]
    data['year'] = ['2018'] * 10

    c = alt.Chart(data).transform_calculate(
        row="ceil(datum.id/10)"
    ).transform_calculate(
        col="datum.id - datum.row*10"
    ).mark_point(
        filled=True,
        size=0.03,
        tooltip=False
    ).encode(
        alt.X("col:O", axis=None),
        alt.Y("row:O", axis=None),
        alt.ShapeValue(car),
        color=alt.Color('color:N',
                        scale=alt.Scale(domain=['kill/injured', 'non'],range=['#5603ad', '#9BA8C7']),
                        legend=None)
    ).properties(
        title=f'In {year}, in average, around {idx} out of 10 Collisions involve injured'
    ).configure_axis(
        grid=False,
        domain=False,
        ticks=False
    ).configure_view(
        strokeWidth=0
    )

    return c