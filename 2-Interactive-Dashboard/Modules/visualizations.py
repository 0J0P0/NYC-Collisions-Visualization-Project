
import pandas as pd
import altair as alt


click = alt.selection_point(fields=['BOROUGH'], toggle='true')

months = alt.selection_multi(fields=['MONTH'], resolve='global')
conditions = alt.selection_multi(fields=['icon'], resolve='global')
vehicles = alt.selection_multi(fields=['VEHICLE TYPE CODE 1', 'COSNT'], resolve='global')


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
    if 'click' in filters:
        c = c.transform_filter(click)

    return c


def legend_chart(df: pd.DataFrame, palette: str = 'category20'):
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
        width=430
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
        width=430
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
        width=430
    )

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

    base_hist = alt.Chart(df).mark_bar(opacity=0.6, binSpacing=0, color='purple')

    ver_hist = base_hist.encode(
        x=alt.X('count():Q',
                title='Collisions'),
        y=alt.Y('WEEKDAY:O',
                # bin=alt.BinParams(maxbins=7),
                sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                axis=None)
    ).properties(
        width=100,
        height=200
    )

    hoz_hist = base_hist.encode(
        x=alt.X('HOUR:O',
                axis=alt.Axis(labels=False, ticks=False, title=None),
                # bin=alt.Bin(maxbins=24)),
        ),
        y=alt.Y('count():Q', title='Collisions')
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

    bars = alt.Chart(df).mark_bar().encode(
        x=alt.X('VEHICLE TYPE CODE 1:N'),
        y=alt.Y('count()'),
        color=alt.Color('VEHICLE TYPE CODE 1:N',
                        scale=alt.Scale(scheme=palette),
                        legend=None),
        column=alt.Column('icon')
    ).properties(
            width=120
        )

    return params_chart(bars, filters)


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