import altair as alt

map_url = 'https://raw.githubusercontent.com/0J0P0/NYC-Collisions-Visualization-Project/main/2-Interactive-Dashboard/Data/new-york-city-zipcodes-ny_.geojson'
map_file = alt.Data(url=map_url, format=alt.DataFormat(property="features"))