import pandas as pd
import altair as alt
import geopandas as gpd


click = alt.selection_point(fields=['BOROUGH'], toggle='true')

months = alt.selection_multi(fields=['MONTH'])
conditions = alt.selection_multi(fields=['icon'])
vehicles = alt.selection_multi(fields=['VEHICLE TYPE CODE 1'])
weekdays = alt.selection_multi(fields=['WEEKDAY'])


def params_chart(c: alt.Chart, filters: list = None):
    """
    Applies the filters to the chart.

    Parameters
    ----------
    c : altair.Chart
        Chart to be filtered.
    filters : list
        List of filters to be applied to the chart.

    Returns
    -------
    altair.Chart
        Filtered chart.
    """


    if filters is None:
        return c

    if 'months' in filters:
        c = c.transform_filter(months)
    if 'conditions' in filters:
        c = c.transform_filter(conditions)
    if 'vehicles' in filters:
        c = c.transform_filter(vehicles)
    if 'weekdays' in filters:
        c = c.transform_filter(weekdays)
    if 'click' in filters:
        c = c.transform_filter(click)

    return c


def legend_chart(df: pd.DataFrame, filters: list = None):
    """
    Creates multiple interactive legends for the dashboard.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the data to be plotted.
    filters : list
        List of filters to be applied to the legends.

    Returns
    -------
    altair.Chart
        Multiple interactive legends for the dashboard.
    """

    month_legend = alt.Chart(df).mark_rect(tooltip=False).encode(
        x = alt.X('MONTH:N',
                title='Month',
                sort=['June', 'July', 'August', 'September'],
                axis=alt.Axis(labelAngle=0, labelFontSize=10)),
        color = alt.condition(months,
                              alt.Color('MONTH:N', legend=None),
                              alt.ColorValue('lightgray'))
    ).add_params(
        months
    ).properties(
        width=250
    )

    condition_legend = alt.Chart(df).mark_rect(tooltip=False).encode(
        x = alt.X('icon:N',
                title='Weather Conditions',
                axis=alt.Axis(labelAngle=0, labelFontSize=10)),
        color = alt.condition(conditions,
                              alt.Color('icon:N', legend=None),
                              alt.ColorValue('lightgray'))
    ).add_params(
        conditions
    ).properties(
        width=250
    )

    vehicle_legend = alt.Chart(df).mark_rect(tooltip=False).encode(
        x = alt.X('VEHICLE TYPE CODE 1:N',
                title='Vehicle Type',
                axis=alt.Axis(labelAngle=0, labelFontSize=10)),
        color = alt.condition(vehicles,
                              alt.Color('VEHICLE TYPE CODE 1:N', legend=None),
                              alt.ColorValue('lightgray'))
    ).add_params(
        vehicles
    ).properties(
        width=150
    )

    weekdays_legend = alt.Chart(df).mark_rect(tooltip=False).encode(
        x = alt.X('WEEKDAY:N',
                title='Day of the Week',
                sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                axis=alt.Axis(labelAngle=0, labelFontSize=10)),
        color = alt.condition(weekdays,
                                alt.Color('WEEKDAY:N', legend=None),
                                alt.ColorValue('lightgray'))
    ).add_params(
        weekdays
    ).properties(
        width=400
    )

    legends = alt.hconcat(month_legend, condition_legend, vehicle_legend, weekdays_legend)

    return legends


def dotmap_chart(df: pd.DataFrame, filters: list = None):
    """
    Creates a dotmap chart with one dot per collision.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the data to be plotted.
    map : altair.topo_feature
        Map to be used in the chart.
    filters : list
        List of filters to be applied to the chart.

    Returns
    -------
    altair.Chart
        Dotmap chart with one dot per collision.
    """

    map_url = 'https://raw.githubusercontent.com/0J0P0/NYC-Collisions-Visualization-Project/main/2-Interactive-Dashboard/Data/new-york-city-zipcodes-ny_.geojson'
    zips = alt.Data(url=map_url, format=alt.DataFormat(property="features"))
    
    nyc = alt.Chart(zips).mark_geoshape(
        stroke='white',
        strokeWidth=1,
        filled=True,
        tooltip=True
    ).encode(
        color=alt.ColorValue('lightblue'),
        opacity=alt.condition(click, alt.value(1), alt.value(0.2)),
        tooltip=[alt.Tooltip('BOROUGH:N'), alt.Tooltip('ZIP CODE:N')]
    ).add_params(
        click
    ).project(
        type='identity', reflectY=True
    ).properties(
        width=500,
        height=500
    )

    points = alt.Chart(df).mark_circle(
        size=10,
        opacity=0.7,
        tooltip=False
    ).encode(
        longitude='LONGITUDE:Q',
        latitude='LATITUDE:Q'
    ).project(
        type='identity', reflectY=True
    ).properties(
        width=500,
        height=500
    )

    points = params_chart(points, filters)

    return nyc + points


def bar_chart(df: pd.DataFrame, filters: list = None):
    """
    Creates a bar chart with the total number of collisions per vehicle type and weather conditions.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the data to be plotted.
    filters : list
        List of filters to be applied to the chart.

    Returns
    -------
    altair.Chart
        Bar chart with the total number of collisions per vehicle type and weather conditions.
    """

    bars = alt.Chart(df).mark_bar(
        tooltip=True
    ).encode(
        x=alt.X('VEHICLE TYPE CODE 1:N', axis=alt.Axis(labelAngle=0, labelFontSize=10), title='Vehicle Type'),
        y=alt.Y('count():Q', title='Collisions'),
        color=alt.Color('VEHICLE TYPE CODE 1:N',
                        legend=None),
        column=alt.Column('icon', title='Weather Conditions'),
        tooltip=[alt.Tooltip('count():Q', title='Collisions'), alt.Tooltip('VEHICLE TYPE CODE 1:N', title='Vehicle Type')]
    ).properties(
    )

    return params_chart(bars, filters)


def hour_line_chart(df: pd.DataFrame, filters: list = None):
    """
    Creates a line chart with the total number of collisions per hour of the day.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the data to be plotted.
    filters : list
        List of filters to be applied to the chart.

    Returns
    -------
    altair.Chart
        Line chart with the total number of collisions per hour of the day.
    """

    line = alt.Chart(df).mark_line(
        tooltip=True
    ).encode(
        x=alt.X('HOUR:O', axis=alt.Axis(labelAngle=0), title='Hour of the Day'),
        y=alt.Y('count():Q', title='Collisions'),
        color=alt.Color('BOROUGH:N'),
        tooltip=[alt.Tooltip('count():Q', title='Collisions'), alt.Tooltip('BOROUGH:N', title='Borough')]
    )

    return params_chart(line, filters)


def day_line_chart(df: pd.DataFrame, filters: list = None):
    """
    Creates a line chart with the total number of collisions per day of the month.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the data to be plotted.
    filters : list
        List of filters to be applied to the chart.

    Returns
    -------
    altair.Chart
        Line chart with the total number of collisions per day of the month.
    """
    
    df_copy = df.copy()
    df_copy['CRASH DATE'] = pd.to_datetime(df_copy['CRASH DATE'])
    df_copy['DAY'] = df_copy['CRASH DATE'].dt.day

    line = alt.Chart(df).mark_area(
        opacity=0.7,
        tooltip=True
    ).encode(
        x=alt.X('DAY:O', axis=alt.Axis(labelAngle=0), title='Day of the Month'),
        y=alt.Y('count():Q', scale=alt.Scale(zero=False), title='Collisions'),
        tooltip=[alt.Tooltip('count():Q', title='Collisions')]
    ).properties(
    )

    return params_chart(line, filters)


def kpi_collisions(df: pd.DataFrame, kpi_text: str, dim: int = 200, filters: list = None):
    """
    Creates a KPI chart with the total number of collisions.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the data to be plotted.
    kpi_text : str
        Text to be displayed in the KPI chart.
    dim : int
        Dimension of the KPI chart.
    filters : list
        List of filters to be applied to the chart.

    Returns
    -------
    altair.Chart
        KPI chart with the total number of collisions.
    """

    text = alt.Chart().mark_text(
        size=dim/6
    ).encode(
        x=alt.value(dim/2),
        y=alt.value(dim/2 - 0.25*dim),
        color=alt.value('black'),
        text=alt.value(kpi_text)
    ).properties(
        width=dim,
        height=dim
    )

    kpi = alt.Chart(df).mark_text(size=dim/5)

    kpi = params_chart(kpi, filters)
    
    kpi = kpi.transform_aggregate(
        count='count()'
    ).encode(
        x=alt.value(dim/2),
        y=alt.value(dim/2),
        color=alt.value('black'),
        text=alt.Text('count:Q')
    ).properties(
        width=dim,
        height=dim
    )

    return text + kpi


def kpi_persons(df: pd.DataFrame, kpi_injured: str, kpi_killed: str, dim: int = 200, filters: list = None):
    """
    Creates two KPI charts with the total number of injured and killed.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the data to be plotted.
    kpi_injured : str
        Text to be displayed in the KPI chart for the total number of injured.
    kpi_killed : str
        Text to be displayed in the KPI chart for the total number of killed.
    dim : int
        Dimension of the KPI chart.
    filters : list
        List of filters to be applied to the chart.

    Returns
    -------
    altair.Chart
        KPI chart with the total number of injured.
    altair.Chart
        KPI chart with the total number of killed.
    """

    text_injured = alt.Chart().mark_text(
        size=dim/6
    ).encode(
        x=alt.value(dim/2),
        y=alt.value(dim/2 - 0.25*dim),
        color=alt.value('black'),
        text=alt.value(kpi_injured)
    ).properties(
        width=dim,
        height=dim
    )

    text_killed = alt.Chart().mark_text(
        size=dim/6
    ).encode(
        x=alt.value(dim/2),
        y=alt.value(dim/2 - 0.25*dim),
        color=alt.value('black'),
        text=alt.value(kpi_killed)
    ).properties(
        width=dim,
        height=dim
    )

    kpi = alt.Chart(df).mark_text(size=dim/5)

    kpi = params_chart(kpi, filters)
    
    kpi_injured = kpi.transform_aggregate(
        injured='sum(TOTAL INJURED)'
    ).encode(
        x=alt.value(dim/2),
        y=alt.value(dim/2),
        color=alt.value('black'),
        text=alt.Text('injured:Q')
    ).properties(
        width=dim,
        height=dim
    )

    kpi_killed = kpi.transform_aggregate(
        killed='sum(TOTAL KILLED)'
    ).encode(
        x=alt.value(dim/2),
        y=alt.value(dim/2),
        color=alt.value('black'),
        text=alt.Text('killed:Q')
    ).properties(
        width=dim,
        height=dim
    )

    return text_injured + kpi_injured, text_killed + kpi_killed


def temp_chart(df: pd.DataFrame, filters: list = None):
    """
    Creates a line chart with the maximum and minimum temperature.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with the data to be plotted.
    filters : list
        List of filters to be applied to the chart.

    Returns
    -------
    altair.Chart
        Line chart with the maximum and minimum temperature.
    """

    brush = alt.selection_interval(encodings=['x'])

    base = alt.Chart(df).mark_line().encode(
        x=alt.X('CRASH DATE:T',
                title='Day of the Month'),
        y=alt.Y('tempmax:Q',
                title='Max - Min Temperature'),
        y2=alt.Y2('tempmin:Q',
                    title=''),
        color=alt.Color('icon:N')
    )

    temp = base.transform_filter(
        brush
    ).properties(
    )

    temp_overview = base.add_params(
        brush
    ).properties(
        height=50
    )

    return params_chart(temp & temp_overview, filters)

