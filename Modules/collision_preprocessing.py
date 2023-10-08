####################################################################################################
__author__ = "Juan P. Zaldivar & Enriq Millan"
__version__ = "1.0.0"
####################################################################################################
"""
This module contains the functions to preprocess the collision data.

Functions:
----------
imputation_with_ref_col(dataset: pd.DataFrame, imputed_col: str, reference_col: str, imputed_value: str, begin=1, end=1) -> None
    This function imputes the values of a column with the values of another column as reference.
"""

####################################################################################################
# IMPORTS ################################################################################ IMPORTS #
####################################################################################################
import os
import numpy as np
import pandas as pd

exists_pre = os.path.isfile('data/collision_clean.csv')

####################################################################################################
# FUNCTIONS ############################################################################ FUNCTIONS #
####################################################################################################
def imputation_with_ref_col(dataset: pd.DataFrame, imputed_col: str, reference_col: str, imputed_value: str, begin=1, end=1) -> None:
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
    begin : int
        The first column to be imputed if there is a range of columns.
    end : int
        The last column to be imputed if there is a range of columns.
    """
    if exists_pre:
        return

    for i in range(begin, end+1):
        dataset[imputed_col + f' {i}'] = dataset.apply(lambda x: imputed_value if not pd.isnull(x[reference_col + f' {i}']) and pd.isnull(x[imputed_col + f' {i}']) else x[imputed_col + f' {i}'], axis=1)