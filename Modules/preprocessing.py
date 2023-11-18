####################################################################################################
__author__ = "Juan P. Zaldivar & Enriq Millan"
__version__ = "1.0.0"
####################################################################################################
"""
This module contains the functions to preprocess the collision and weather datasets.

Functions:
----------

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
    if 5 <= int(hour) < 12:
        return "Morning"
    elif 12 <= int(hour) < 18:
        return "Afternoon"
    else:
        return "Night"
    

def cluterize_vehicle_type(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
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