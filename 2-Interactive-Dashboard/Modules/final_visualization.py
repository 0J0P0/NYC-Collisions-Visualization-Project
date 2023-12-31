import pandas as pd
import altair as alt



months = alt.selection_multi(fields=['MONTH'])
conditions = alt.selection_multi(fields=['ICON'])
weekdays = alt.selection_multi(fields=['WEEKDAY'])
vehicles = alt.selection_multi(fields=['VEHICLE TYPE CODE 1'])
boroughs = alt.selection_multi(fields=['BOROUGH'])


def legend_chart(df: pd.DataFrame):
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

    df = df[['BOROUGH', 'VEHICLE TYPE CODE 1', 'MONTH', 'WEEKDAY', 'ICON']]

    month_legend = alt.Chart(df).mark_rect(tooltip=False).encode(
        x = alt.X('MONTH:N',
                title='Month',
                sort=['June', 'July', 'August', 'September'],
                axis=alt.Axis(labelAngle=0, labelFontSize=10)),
        color = alt.condition(months,
                              alt.Color('MONTH:N', scale=alt.Scale(scheme='category20'), legend=None),
                              alt.ColorValue('lightgray'))
    ).add_params(
        months
    ).properties(
        width=584
    )

    condition_legend = alt.Chart(df).mark_rect(tooltip=False).encode(
        x = alt.X('ICON:N',
                title='Weather Conditions',
                axis=alt.Axis(labelAngle=0, labelFontSize=10)),
        color = alt.condition(conditions,
                              alt.Color('ICON:N', scale=alt.Scale(scheme='category20'), legend=None),
                              alt.ColorValue('lightgray'))
    ).add_params(
        conditions
    ).properties(
        width=584
    )

    vehicle_legend = alt.Chart(df).mark_rect(tooltip=False).encode(
        x = alt.X('VEHICLE TYPE CODE 1:N',
                title='Vehicle Type',
                axis=alt.Axis(labelAngle=0, labelFontSize=10)),
        color = alt.condition(vehicles,
                              alt.Color('VEHICLE TYPE CODE 1:N', scale=alt.Scale(domain=['Ambulance', 'Fire', 'Taxi'], range=['#9C9EDE', '#F7B6D2', '#AEC7E8']), legend=None),
                              alt.ColorValue('lightgray'))
    ).add_params(
        vehicles
    ).properties(
        width=400
    )

    weekdays_legend = alt.Chart(df).mark_rect(tooltip=False).encode(
        x = alt.X('WEEKDAY:N',
                title='Day of the Week',
                sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                axis=alt.Axis(labelAngle=0, labelFontSize=10)),
        color = alt.condition(weekdays,
                                alt.Color('WEEKDAY:N', scale=alt.Scale(scheme='category20'), legend=None),
                                alt.ColorValue('lightgray'))
    ).add_params(
        weekdays
    ).properties(
        width=768
    )

    boroughs_legend = alt.Chart(df).mark_rect(tooltip=False).encode(
        x = alt.X('BOROUGH:N',
                title='',
                axis=alt.Axis(labelAngle=0, labelFontSize=10, orient='top')),
        color = alt.condition(boroughs,
                                alt.Color('BOROUGH:N', scale=alt.Scale(domain=['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island'], range=['#393B79', '#D62728', '#7B4173', '#FFBB78', '#AEC7E8']), legend=None),
                                alt.ColorValue('lightgray'))
    ).add_params(
        boroughs
    ).properties(
        width=500
    )

    legends = alt.vconcat(alt.hconcat(month_legend, condition_legend), alt.hconcat(vehicle_legend, weekdays_legend).resolve_scale(color='independent'))

    return legends, boroughs_legend


def dotmap_chart(df: pd.DataFrame):
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
    
    def determine_injured_or_killed(row):
        if row['TOTAL KILLED'] > 0:
            return 'Killed'
        elif row['TOTAL INJURED'] > 0:
            return 'Injured'
        else:
            return 'None'

    df['INJURED/KILLED'] = df.apply(determine_injured_or_killed, axis=1)

    df = df[['LONGITUDE', 'LATITUDE', 'BOROUGH', 'VEHICLE TYPE CODE 1', 'MONTH', 'WEEKDAY', 'ICON', 'INJURED/KILLED']]


    nyc = alt.Chart(zips).mark_geoshape(
        stroke='white',
        strokeWidth=1,
        filled=True,
        tooltip=True
    ).encode(
        color=alt.ColorValue('#AEC7E8'),
        tooltip=[alt.Tooltip('properties.borough:N', title='BOROUGH'), alt.Tooltip('.properties.postalCode:N', title='ZIP CODE')]
    ).project(
        type='identity', reflectY=True
    ).properties(
        width=500,
        height=500
    )

    points = alt.Chart(df).mark_point(
        filled=True,
        tooltip=False
    ).encode(
        longitude='LONGITUDE:Q',
        latitude='LATITUDE:Q',
        color=alt.Color('INJURED/KILLED:N', scale=alt.Scale(domain=['Killed', 'Injured', 'None'], range=['purple', 'green', 'blue']), legend=alt.Legend(title='Casualties', orient='top')),
        opacity=alt.condition(alt.datum['INJURED/KILLED'] == 'Killed', alt.value(1), alt.value(0.3)),
        size=alt.condition(alt.datum['INJURED/KILLED'] == 'Killed', alt.value(50), alt.value(10)),
        shape=alt.condition(alt.datum['INJURED/KILLED'] == 'Killed', alt.value('triangle'), alt.value('circle')),
    ).project(
        type='identity', reflectY=True
    ).properties(
        width=500,
        height=500
    )

    points = points.transform_filter(
        months
    ).transform_filter(
        conditions
    ).transform_filter(
        vehicles
    ).transform_filter(
        weekdays
    ).transform_filter(
        boroughs
    )

    return (nyc + points)


def bar_chart(df: pd.DataFrame):
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

    df = df[['BOROUGH', 'VEHICLE TYPE CODE 1', 'MONTH', 'WEEKDAY', 'ICON']]

    bars = alt.Chart(df).mark_bar(
        tooltip=True
    ).encode(
        x=alt.X('VEHICLE TYPE CODE 1:N', axis=alt.Axis(labelAngle=0, labelFontSize=10), title='Vehicle Type'),
        y=alt.Y('count():Q', title='Collisions'),
        color=alt.Color('VEHICLE TYPE CODE 1:N', scale=alt.Scale(domain=['Ambulance', 'Fire', 'Taxi'], range=['#9C9EDE', '#F7B6D2', '#AEC7E8']), legend=None),
        column=alt.Column('ICON', title='Weather Conditions'),
        tooltip=[alt.Tooltip('count():Q', title='Collisions'), alt.Tooltip('VEHICLE TYPE CODE 1:N', title='Vehicle Type')]
    ).properties(
        width=133,
        height=370
    )

    bars = bars.transform_filter(
        months
    ).transform_filter(
        conditions
    ).transform_filter(
        vehicles
    ).transform_filter(
        weekdays
    ).transform_filter(
        boroughs
    )

    return bars


def hour_line_chart(df: pd.DataFrame):
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

    df = df[['BOROUGH', 'VEHICLE TYPE CODE 1', 'HOUR', 'MONTH', 'WEEKDAY', 'ICON']] 

    line = alt.Chart(df).mark_line(
        point=True,
        tooltip=True
    ).encode(
        x=alt.X('HOUR:O', axis=alt.Axis(labelAngle=0, grid=True), title='Hour of the Day'),
        y=alt.Y('count():Q', title='Collisions'),
        color=alt.Color('BOROUGH:N', scale=alt.Scale(domain=['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island'], range=['#393B79', '#D62728', '#7B4173', '#FFBB78', '#AEC7E8']), legend=None),
        tooltip=[alt.Tooltip('count():Q', title='Collisions'), alt.Tooltip('BOROUGH:N', title='Borough')]
    )

    line = line.transform_filter(
        months
    ).transform_filter(
        conditions
    ).transform_filter(
        vehicles
    ).transform_filter(
        weekdays
    ).transform_filter(
        boroughs    
    ).add_params(
        boroughs
    )

    return line


def day_line_chart(df: pd.DataFrame):
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

    df_copy = df_copy[['BOROUGH', 'VEHICLE TYPE CODE 1', 'DAY', 'MONTH', 'WEEKDAY', 'ICON']]

    base = alt.Chart(df_copy)

    line = base.mark_area(
        opacity=0.7,
        interpolate='monotone',
        tooltip=True
    ).encode(
        x=alt.X('DAY:O', axis=alt.Axis(labelAngle=0, grid=True), title='Day of the Month'),
        y=alt.Y('count():Q', scale=alt.Scale(zero=False), title='Collisions'),
        color=alt.value('purple'),
        tooltip=[alt.Tooltip('count():Q', title='Collisions'), alt.Tooltip('DAY:O', title='Day of the Month')]
    ).properties(
        width=600,
        height=300
    )

    rule = base.mark_rule(
        color='red'
    ).transform_aggregate(
        count='count()',
        groupby=['DAY']
    ).encode(
        y='max(count):O'
    )

    # line = line + rule

    line = line.transform_filter(
        months
    ).transform_filter(
        conditions
    ).transform_filter(
        vehicles
    ).transform_filter(
        weekdays
    ).transform_filter(
        boroughs
    )

    return line


def kpi_collisions(df: pd.DataFrame, dim: int = 200):
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

    df = df[['BOROUGH', 'VEHICLE TYPE CODE 1', 'MONTH', 'WEEKDAY', 'ICON']]

    kpi = alt.Chart(df).mark_text(size=dim/5)

    kpi = kpi.transform_filter(
        months
    ).transform_filter(
        conditions
    ).transform_filter(
        vehicles
    ).transform_filter(
        weekdays
    ).transform_filter(
        boroughs
    )
    
    kpi = kpi.transform_aggregate(
        count='count()'
    ).encode(
        x=alt.value(dim/2-0.35*dim),
        y=alt.value((dim/4)/2-0.3*(dim/4)),
        color=alt.value('black'),
        text=alt.Text('count:Q')
    ).properties(
        width=dim,
        height=dim/4,
        title='Collisions'
    )

    return kpi


def kpi_persons(df: pd.DataFrame, dim: int = 200):
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

    df = df[['BOROUGH', 'VEHICLE TYPE CODE 1', 'MONTH', 'WEEKDAY', 'ICON', 'TOTAL INJURED', 'TOTAL KILLED']]

    kpi = alt.Chart(df).mark_text(size=dim/5)

    kpi = kpi.transform_filter(
        months
    ).transform_filter(
        conditions
    ).transform_filter(
        vehicles
    ).transform_filter(
        weekdays
    ).transform_filter(
        boroughs
    )
    
    kpi_injured = kpi.transform_aggregate(
        injured='sum(TOTAL INJURED)'
    ).encode(
        x=alt.value(dim/2-0.35*dim),
        y=alt.value((dim/4)/2-0.3*(dim/4)),
        color=alt.value('black'),
        text=alt.Text('injured:Q')
    ).properties(
        width=dim,
        height=(dim/4),
        title='Injured'
    )

    kpi_killed = kpi.transform_aggregate(
        killed='sum(TOTAL KILLED)'
    ).encode(
        x=alt.value(dim/2-0.35*dim),
        y=alt.value((dim/4)/2-0.3*(dim/4)),
        color=alt.value('black'),
        text=alt.Text('killed:Q')
    ).properties(
        width=dim,
        height=(dim/4),
        title='Killed'
    )

    return (kpi_injured), (kpi_killed)

