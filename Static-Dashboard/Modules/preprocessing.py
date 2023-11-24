####################################################################################################
__author__ = "Juan P. Zaldivar & Enric Millan"
__version__ = "1.0.0"
####################################################################################################

"""
This module contains the functions to preprocess the collision and weather datasets.

Functions:
----------

time_filter(dataset: pd.DataFrame, time_col: str) -> pd.DataFrame
    This function filters the dataset by a time column to get the data of the summer months of 2018 and 2020.

categorize_moment(hour: str) -> str
    This function categorizes the time of the day. The categories are: Morning, Afternoon and Night.

clusterize_vehicle_type(df: pd.DataFrame, col: str) -> pd.DataFrame
    This function clusters the vehicle types in the dataset.

imputation_with_ref_col(dataset: pd.DataFrame, imputed_col: str, reference_col: str, imputed_value: str) -> None
    This function imputes the values of a column with the values of another column as reference.

beaufort_scale(wind_speed_mps: float) -> str
    This function categorizes the wind speed according to the Beaufort Scale.

rain_intensity_scale(prcp_mm: float) -> str
    This function categorizes the rain intensity according to the rain intensity scale.
"""

####################################################################################################
# IMPORTS ################################################################################ IMPORTS #
####################################################################################################
import pandas as pd


####################################################################################################
# FUNCTIONS ############################################################################ FUNCTIONS #
####################################################################################################
def time_filter(dataset: pd.DataFrame, time_col: str) -> pd.DataFrame:
    """
    This function filters the dataset by a time column to get the data of the summer months of 2018 and 2020.

    Parameters
    ----------
    dataset : pd.DataFrame
        The dataset to be filtered.
    time_col : str
        The column to be used as reference.

    Returns
    -------
    pd.DataFrame
        The filtered dataset.
    """
    dataset = dataset[((dataset[time_col] >= '2018-06-01') & (dataset[time_col] <= '2018-09-30')) | ((dataset[time_col] >= '2020-06-01') & (dataset[time_col] <= '2020-09-30'))]

    return dataset


def categorize_moment(hour):
    """
    This function categorizes the time of the day. The categories are: Morning, Afternoon and Night.

    Parameters
    ----------
    hour : str
        The hour to be categorized.

    Returns
    -------
    str
        The category of the hour.
    """
    
    if 5 <= int(hour) < 12:
        return "Morning"
    elif 12 <= int(hour) < 18:
        return "Afternoon"
    else:
        return "Night"
    

def clusterize_vehicle_type(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    This function clusters the vehicle types in the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to be clustered.
    col : str
        The column to be clustered.
    
    Returns
    -------
    pd.DataFrame
        The clustered dataset.
    """

    df[col] = df[col].replace(['SUV', 'FLAT', '3-DOOR', 'CHEVY EXPR', 'PC', 'ELEC. UNIC', 'E REVEL SC','F150XL PIC', '2- TO', 'NEW Y', 'STREE', 'RGS', 'OMR', 'DEMA-', 'BK', 'NYPD'], 'CAR')

    df[col] = df[col].replace(['99999'], 'UNKNOWN')

    df[col] = df[col].replace(['BULK AGRICULTURE', 'PK', 'TANK', 'SLINGSHOT', 'UTV', 'JOHN DEERE', '1C', 'STAK', 'PALLET', 'SPRIN', 'ACCES'], 'OTHERS')

    df[col] = df[col].replace(['BOX', 'DOT EQUIPM', 'DRILL RIG', 'PAS', 'LOADE', 'SGWS', 'HEAVY'], 'TRUCK')

    df[col] = df[col].replace(['MOTORIZED HOME', 'CHASSIS CAB', 'SWT', 'MESSAGE SI', 'RV', 'UHAUL', 'POSTO'], 'VAN')

    df[col] = df[col].replace(['MOPED', 'J1'], 'MOTORCYCLE')

    df[col] = df[col].replace(['SANIT'], 'AMBULANCE')

    df[col].fillna('UNKNOWN', inplace=True)

    return df


def imputation_with_ref_col(dataset: pd.DataFrame, imputed_col: str, reference_col: str, imputed_value: str) -> None:
    """
    This function imputes the values of a column with the values of another column as reference.

    Parameters
    ----------
    dataset : pd.DataFrame
        The dataset to be imputed.
    imputed_col : str
        The column to be imputed.
    reference_col : str
        The column to be used as reference.
    imputed_value : str
        The value to be imputed.
    """
    
    dataset[imputed_col] = dataset.apply(lambda x: imputed_value if not pd.isnull(x[reference_col]) and pd.isnull(x[imputed_col]) else x[imputed_col], axis=1)


def beaufort_scale(wind_speed_mps: float) -> str:
    """
    This function categorizes the wind speed according to the Beaufort Scale.

    Parameters
    ----------
    wind_speed_mps : float
        The wind speed to be categorized.
    
    Returns
    -------
    str
        The category of the wind speed.
    """

    if wind_speed_mps < 0.3:
        return "Calm"
    elif wind_speed_mps < 1.5:
        return "Light Air"
    elif wind_speed_mps < 3.4:
        return "Light Breeze"
    elif wind_speed_mps < 5.5:
        return "Gentle Breeze"
    elif wind_speed_mps < 8.0:
        return "Moderate Breeze"
    elif wind_speed_mps < 10.8:
        return "Fresh Breeze"
    elif wind_speed_mps < 13.9:
        return "Strong Breeze"
    elif wind_speed_mps < 17.2:
        return "Near Gale"
    elif wind_speed_mps < 20.8:
        return "Gale"
    elif wind_speed_mps < 24.5:
        return "Strong Gale"
    elif wind_speed_mps < 28.5:
        return "Storm"
    else:
        return "Hurricane"
    

def rain_intensity_scale(prcp_mm: float) -> str:
    """
    This function categorizes the rain intensity according to the rain intensity scale.

    Parameters
    ----------
    prcp_mm : float
        The rain intensity to be categorized.
    
    Returns
    -------
    str
        The category of the rain intensity.
    """

    if prcp_mm < 2.5*24:
        return "Slight"
    elif prcp_mm < 10*24:
        return "Moderate"
    elif prcp_mm < 50*24:
        return "Heavy"
    else:
        return "Violent"