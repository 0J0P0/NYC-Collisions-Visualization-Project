####################################################################################################
#                                                                                                  #
#   Module: preprocessing.py                                                                       #
#   Description: Functions used to preprocess the data                                             #
#                                                                                                  #
####################################################################################################


####################################################################################################
#                                                                                                  #
#   Libraries                                                                                      #
#                                                                                                  #
###################################################################################################

import time
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.geocoders import Nominatim


####################################################################################################
#                                                                                                  #
#   Functions                                                                                      #
#                                                                                                  #
####################################################################################################

def capitalize_street(street_name):
    """
    Capitalize the street name
    
    Parameters
    ----------
    street_name : str
        Street name to be capitalized
        
    Returns
    -------
    street : str
        Capitalized street name
    """

    street = ''
    for word in street_name.split():
        street += word.capitalize() + ' '
    
    return street.strip()   


def fill_missing_coordinates(row):
    """
    Fill missing coordinates using the street name, borough and zip code

    Parameters
    ----------
    row : pandas.Series
        Row of the dataframe
    
    Returns
    -------
    row : pandas.Series
        Row of the dataframe with the filled coordinates
    """

    geolocator = Nominatim(user_agent="my_geocoder")

    street_name = row['STREET NAME']
    latitude = row['LATITUDE']
    longitude = row['LONGITUDE']
    
    if pd.isnull(latitude) or pd.isnull(longitude):
        try:
            borough = row['BOROUGH']
            if not pd.isnull(borough):
                street_name = street_name + ', ' + borough
            zip_code = row['ZIP CODE']
            if not pd.isnull(zip_code):
                street_name = street_name + ', ' + str(int(zip_code))

            time.sleep(1)

            location = geolocator.geocode(street_name + ', New York City')
            if location:
                row['LATITUDE'] = location.latitude
                row['LONGITUDE'] = location.longitude
        except Exception as e:
            print(f"Error: {e}")
    
    return row


def get_borough_polygons():
    """
    Get the polygon of each borough of New York City

    Returns
    -------
    borough_poly : dict
        Dictionary containing the polygon of each borough
    """

    nyc_map = gpd.read_file('Data/new-york-city-boroughs-ny_.geojson')

    boroughs = ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']

    borough_poly = {}
    for b in boroughs:
        poly = nyc_map[nyc_map['name'] == b]['geometry']
        borough_poly[b] = poly.values[0]

    return borough_poly


def get_zip_polygons():
    """
    Get the polygon of each zip code of New York City

    Returns
    -------
    zip_poly : dict
        Dictionary containing the polygon of each zip code
    """

    nyc_map = gpd.read_file('Data/new-york-city-zipcodes-ny_.geojson')

    zips = nyc_map['postalCode'].unique().tolist()

    # Extraction of the zips polygon
    zip_poly = {}
    for z in zips:
        poly = nyc_map[nyc_map['postalCode'] == z]['geometry']
        zip_poly[z] = poly.values[0]

    return zip_poly


def fill_missing_borough_zip(df, borough_poly, zip_poly):
    """
    Fill missing borough and zip code using the coordinates

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the data

    borough_poly : dict
        Dictionary containing the polygon of each borough
    
    zip_poly : dict
        Dictionary containing the polygon of each zip code
    
    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the data with the filled borough and zip code
    """

    for idx, row in df.iterrows():
        lon = row['LONGITUDE']
        lat = row['LATITUDE']
        
        if row['BOROUGH'] is not None:

            if lat is not None and lon is not None:
                p = Point(lon, lat)
                for b, poly in borough_poly.items():
                    if p.within(poly):
                        df.loc[idx, 'BOROUGH'] = b.upper()
                        break
        
        if row['ZIP CODE'] is not None:
            if lat is not None and lon is not None:
                p = Point(lon, lat)
                for z, poly in zip_poly.items():
                    if p.within(poly):
                        df.loc[idx, 'ZIP CODE'] = z
                        break
