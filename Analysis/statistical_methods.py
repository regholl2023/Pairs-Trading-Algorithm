import os
import sys

import numpy as np
import pandas as pd
import yfinance as yf
from statsmodels.regression.rolling import RollingOLS
from statsmodels.tsa.stattools import adfuller

# Directory Path Setup
"""Get the directory of the current script. If the script is not in the root directory, navigate to the root 
directory and append it to sys.path for module imports."""
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

# Custom Module Imports
from AidanUtils.MyTimer import timeit
from Analysis.DATES import Dates


def collect_metrics_for_pair(stock_1, stock_2) -> pd.DataFrame:
    """
    Downloads and processes financial data for a pair of stocks.
    Calculates returns, forward returns, hedge ratio using rolling OLS, spread, rolling correlation, and z-score.
    Classifies z-scores into trading signals.
    """
    stock_data_df = yf.download(tickers=[stock_1, stock_2], start=Dates.START_DATE.value, end=Dates.END_DATE.value)
    stock_data_df = stock_data_df.stack()
    # Additional processing and calculations follow...


def adf_test(stock_1, stock_2) -> bool:
    """
    Performs the Augmented Dickey-Fuller test on the spread of two stocks to assess stationarity.
    Returns True if the spread is stationary, False otherwise.
    """
    removed_na_df = collect_metrics_for_pair(stock_1, stock_2)
    adf_result = adfuller(removed_na_df['spread'])[1]
    return adf_result <= 0.05


@timeit
def run_adf_on_best_pairs(highest_corr_pairs) -> list:
    """
    Applies the ADF test on pairs of stocks with the highest correlation.
    Returns a list of results indicating whether each pair's spread is stationary.
    """
    adf_list = []
    for n in range(len(highest_corr_pairs)):
        result = adf_test(highest_corr_pairs['Stock_1'][n], highest_corr_pairs['Stock_2'][n])
        adf_list.append(result)
    return adf_list
