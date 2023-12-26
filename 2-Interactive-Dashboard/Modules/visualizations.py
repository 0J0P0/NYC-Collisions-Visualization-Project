
import pandas as pd
import altair as alt


click = alt.selection_point(fields=['BOROUGH'], toggle='true')

months = alt.selection_multi(fields=['MONTH'])
conditions = alt.selection_multi(fields=['icon'])
vehicles = alt.selection_multi(fields=['VEHICLE TYPE CODE 1'])
weekdays = alt.selection_multi(fields=['WEEKDAY'])


def params_chart(c: alt.Chart, filters: list = None):
    """
    .
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


def legend_chart(df: pd.DataFrame, palette: str = 'category20', filters: list = None):
    """
    .
    """

    month_legend = alt.Chart(df).mark_rect().encode(
        x = alt.X('MONTH:N',
                title='Month',
                sort=['June', 'July', 'August', 'September'],
                axis=alt.Axis(labelAngle=0)),
        color = alt.condition(months,
                              alt.Color('MONTH:N', scale=alt.Scale(scheme=palette), legend=None),
                              alt.ColorValue('lightgray'))
    ).add_params(
        months
    ).properties(
        # width=430
    )

    condition_legend = alt.Chart(df).mark_rect().encode(
        x = alt.X('icon:N',
                title='Weather Conditions',
                axis=alt.Axis(labelAngle=0)),
        color = alt.condition(conditions,
                              alt.Color('icon:N', scale=alt.Scale(scheme=palette), legend=None),
                              alt.ColorValue('lightgray'))
    ).add_params(
        conditions
    ).properties(
        # width=430
    )

    vehicle_legend = alt.Chart(df).mark_rect().encode(
        x = alt.X('VEHICLE TYPE CODE 1:N',
                title='Vehicle Type',
                axis=alt.Axis(labelAngle=0)),
        color = alt.condition(vehicles,
                              alt.Color('VEHICLE TYPE CODE 1:N', scale=alt.Scale(scheme=palette), legend=None),
                              alt.ColorValue('lightgray'))
    ).add_params(
        vehicles
    ).properties(
        # width=430
    )

    weekdays_legend = alt.Chart(df).mark_rect().encode(
        x = alt.X('WEEKDAY:N',
                title='Day of the Week',
                sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                axis=alt.Axis(labelAngle=0)),
        color = alt.condition(weekdays,
                                alt.Color('WEEKDAY:N', scale=alt.Scale(scheme=palette), legend=None),
                                alt.ColorValue('lightgray'))
    ).add_params(
        weekdays
    ).properties(
        # width=430
    )

    if filters is not None and 'weekdays' in filters:
        legends = alt.hconcat(month_legend, condition_legend, vehicle_legend, weekdays_legend)
    else:
        legends = alt.hconcat(month_legend, condition_legend, vehicle_legend)

    return legends


def heatmap_chart(df: pd.DataFrame, palette: str = 'blues', filters: list = None):
    """
    .
    """

    heat = alt.Chart(df).mark_rect().encode(
        x=alt.X('HOUR:O',
                axis=alt.Axis(labelAngle=0),
                title='Hour of the Day'),
        y=alt.Y('WEEKDAY:O',
                sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                title='Day of the Week'),
        color=alt.Color('count():Q',
                        legend=None,
                        scale=alt.Scale(scheme=palette)),
    ).properties(
        width=600,
        height=200
    )

    base_hist = alt.Chart(df).mark_bar(opacity=0.6, binSpacing=0, color='purple', tooltip=True)

    ver_hist = base_hist.encode(
        x=alt.X('count():Q',
                title='Collisions'),
        y=alt.Y('WEEKDAY:O',
                # bin=alt.BinParams(maxbins=7),
                sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                axis=None),
        tooltip=[alt.Tooltip('count():Q', title='Collisions'), alt.Tooltip('WEEKDAY:O', title='Day of the Week')]
    ).properties(
        width=100,
        height=200
    )

    hoz_hist = base_hist.encode(
        x=alt.X('HOUR:O',
                axis=alt.Axis(labels=False, ticks=False, title=None),
                # bin=alt.Bin(maxbins=24)),
        ),
        y=alt.Y('count():Q', title='Collisions'),
        tooltip=[alt.Tooltip('count():Q', title='Collisions'), alt.Tooltip('HOUR:O', title='Hour of the Day')]
    ).properties(
        width=600,
        height=50
    )

    text = heat.mark_text().encode(
        text=alt.Text('count():Q'),
        color=alt.ColorValue('white')
    ).properties(
        width=600,
        height=200
    )

    heatmap = heat + text
    heatmap = hoz_hist & (heatmap | ver_hist)

    return params_chart(heatmap, filters)


def dotmap_chart(df: pd.DataFrame, map, filters: list = None):
    """
    .
    """

    nyc = alt.Chart(map).mark_geoshape(
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
        latitude='LATITUDE:Q',
        color=alt.value('purple')
    ).project(
        type='identity', reflectY=True
    ).properties(
        width=500,
        height=500
    )

    points = params_chart(points, filters)

    return nyc + points


def scatter_chart(df: pd.DataFrame, palette: str = 'blues', filters: list = None):
    """
    .
    """

    temp = alt.Chart(df).mark_point(
        filled=True,
        size=80
    ).encode(
        x=alt.X('CRASH DATE:T'),
        y=alt.Y('count()', scale=alt.Scale(zero=False)),
        color=alt.Color('temp:Q',
                        scale=alt.Scale(scheme=palette),
                        legend=alt.Legend(title="Temperature")),
    ).properties(
        width=700
    )

    return params_chart(temp, filters)


def bar_chart(df: pd.DataFrame, palette: str = 'category20', filters: list = None):
    """
    .
    """

    bars = alt.Chart(df).mark_bar(
        tooltip=True
    ).encode(
        x=alt.X('VEHICLE TYPE CODE 1:N', axis=alt.Axis(labelAngle=0, labelFontSize=10), title='Vehicle Type'),
        y=alt.Y('count():Q', title='Collisions'),
        color=alt.Color('VEHICLE TYPE CODE 1:N',
                        scale=alt.Scale(scheme=palette),
                        legend=None),
        column=alt.Column('icon', title='Weather Conditions'),
        tooltip=[alt.Tooltip('count():Q', title='Collisions'), alt.Tooltip('VEHICLE TYPE CODE 1:N', title='Vehicle Type')]
    ).properties(
            width=165
    )

    return params_chart(bars, filters)


def hour_line_chart(df: pd.DataFrame, palette: str = 'category20', filters: list = None):
    """
    .
    """

    line = alt.Chart(df).mark_line(
        tooltip=True
    ).encode(
        x=alt.X('HOUR:O', axis=alt.Axis(labelAngle=0), title='Hour of the Day'),
        y=alt.Y('count():Q', title='Collisions'),
        color=alt.Color('BOROUGH:N', scale=alt.Scale(scheme=palette)),
        tooltip=[alt.Tooltip('count():Q', title='Collisions'), alt.Tooltip('BOROUGH:N', title='Borough')]
    ).properties(
        
    )

    return params_chart(line, filters)


def day_line_chart(df: pd.DataFrame, palette: str = 'category20', filters: list = None):
    """
    .
    """
    
    df['CRASH DATE'] = pd.to_datetime(df['CRASH DATE'])
    df['DAY'] = df['CRASH DATE'].dt.day

    line = alt.Chart(df).mark_line(
        tooltip=True
    ).encode(
        x=alt.X('DAY:O', axis=alt.Axis(labelAngle=0), title='Day of the Month'),
        y=alt.Y('count():Q'),
        tooltip=[alt.Tooltip('count():Q', title='Collisions')]
    ).properties(
        width=750
    )

    return params_chart(line, filters)


def kpi_chart(df: pd.DataFrame, text: str, fill: int = 0, dim: int = 200, fillcolor: str = 'lightblue', filters: list = None):
    """
    .
    """
    df = pd.DataFrame({
        'category': ['empty', 'filled'],
        'value': [fill, 1-fill]
    })

    rad = alt.Chart(df).mark_arc(
        innerRadius=dim/3
    ).transform_calculate(

    ).encode(
            theta='value',
            color=alt.Color('category:O', scale=alt.Scale(range=[f'{fillcolor}', 'lightgray']), legend=None),
        ).properties(
            width=dim,
            height=dim
        )

    text_rad = rad.mark_text(size=dim/len(text)).encode(
        x=alt.value(dim/2),
        y=alt.value(dim/2),
        color=alt.value('black'),
        text=alt.value(text)
    )

    return params_chart(rad, filters)


def kpi_collisions(df: pd.DataFrame, kpi_text: str, dim: int = 200, filters: list = None):
    """
    .
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
    .
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
        sum='sum(TOTAL INJURED)'
    ).encode(
        x=alt.value(dim/2),
        y=alt.value(dim/2),
        color=alt.value('black'),
        text=alt.Text('sum:Q')
    ).properties(
        width=dim,
        height=dim
    )

    kpi_killed = kpi.transform_aggregate(
        sum='sum(TOTAL KILLED)'
    ).encode(
        x=alt.value(dim/2),
        y=alt.value(dim/2),
        color=alt.value('black'),
        text=alt.Text('sum:Q')
    ).properties(
        width=dim,
        height=dim
    )

    return text_injured + kpi_injured, text_killed + kpi_killed


def bulltet_chart(df: pd.DataFrame, filters: list = None):
    """
    .
    """

    total = df.shape[0]
    total_injured = df['TOTAL INJURED'].sum()
    total_killed = df['TOTAL KILLED'].sum()

    total_tick = alt.Chart().mark_tick(
        thickness=2,
        color='black'
    ).transform_calculate(
        total=str(total)
    ).encode(
        x=alt.X('total:Q', title='')
    )

    injured_tick = alt.Chart().mark_tick(
        thickness=2,
        color='black'
    ).transform_calculate(
        total=str(total_injured)
    ).encode(
        x=alt.X('total:Q', title='')
    )

    killed_tick = alt.Chart().mark_tick(
        thickness=2,
        color='black'
    ).transform_calculate(
        total=str(total_killed)
    ).encode(
        x=alt.X('total:Q', title='')
    )


    total_bar = alt.Chart(df).mark_bar(
        size=20,
        color='lightblue',
        tooltip=True
    ).encode(
        x=alt.X('count():Q'),
        tooltip=[alt.Tooltip('count():Q', title='Collisions')]
    )

    injured_bar = alt.Chart(df).mark_bar(
        size=20,
        color='lightblue',
        tooltip=True
    ).encode(
        x=alt.X('sum(TOTAL INJURED):Q'),
        tooltip=[alt.Tooltip('sum(TOTAL INJURED):Q', title='Injured')]
    )

    killed_bar = alt.Chart(df).mark_bar(
        size=20,
        color='lightblue',
        tooltip=True
    ).encode(
        x=alt.X('sum(TOTAL KILLED):Q'),
        tooltip=[alt.Tooltip('sum(TOTAL KILLED):Q', title='Killed')]
    )

    total_bar = params_chart(total_bar, filters)
    injured_bar = params_chart(injured_bar, filters)
    killed_bar = params_chart(killed_bar, filters)

    c1 = alt.layer(total_tick, total_bar).properties(height=30, width=500, title='Total Collisions')
    c2 = alt.layer(injured_tick, injured_bar).properties(height=30, width=500, title='Total Injured')
    c3 = alt.layer(killed_tick, killed_bar).properties(height=30, width=500, title='Total Killed')

    return c1 & c2 & c3