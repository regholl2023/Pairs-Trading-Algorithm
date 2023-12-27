import os
import sys
import time

import numpy as np
import pandas as pd
import yfinance as yf
from statsmodels.regression.rolling import RollingOLS
from statsmodels.tsa.stattools import adfuller

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# If the script is not in the root directory, navigate to the root directory
root_dir = os.path.dirname(current_dir)
# Append the root directory to sys.path so that modules can be imported
sys.path.append(root_dir)

from AidanUtils.MyTimer import timeit
from AidanUtils.ProgressBar import print_progress_bar
from Analysis.Dates import Dates


def classify_zscore(df: pd.DataFrame) -> int:
    if df['z_score'] < -1:
        return 1
    elif df['z_score'] > 1:
        return -1
    else:
        return 0


def collect_metrics_for_pair(stock_1, stock_2):
    # Downloading the required data
    stock_data_df = yf.download(tickers=[stock_1, stock_2], start=Dates.START_DATE.value, end=Dates.END_DATE.value)
    stock_data_df = stock_data_df.stack()

    # Finding the required metrics
    stock_data_df['return'] = (stock_data_df['Adj Close'] - stock_data_df['Open']) / stock_data_df['Open']
    stock_data_df['forward_return'] = stock_data_df.groupby(level=1)['return'].transform(lambda x: x.shift(-1))
    stock_data_df = stock_data_df[['Adj Close', 'forward_return']].unstack().droplevel(axis=1, level=0)
    stock_data_df.columns = [stock_1, stock_2, f'{stock_1}_forward_return', f'{stock_2}_forward_return']
    stock_data_df[f'{stock_1}_return'] = np.log(stock_data_df[stock_1]).diff()
    stock_data_df[f'{stock_2}_return'] = np.log(stock_data_df[stock_2]).diff()

    # Calculating the hedge ration using a rolling OLS regression
    stock_data_df['hedge_ratio'] = RollingOLS(stock_data_df[f'{stock_2}_return'],
                                              stock_data_df[f'{stock_1}_return'],
                                              window=60).fit().params.values

    # Calculating the spread of stock 1 and stock 2 price
    stock_data_df['spread'] = (stock_data_df[stock_1] - stock_data_df[stock_2] * stock_data_df['hedge_ratio'])

    # Rolling Correlation test
    stock_data_df['roll_corr'] = stock_data_df[stock_1].rolling(180).corr(stock_data_df[stock_2])

    def smooth_zscore(spread):
        return (spread.rolling(1).mean() - spread.rolling(50).mean()) / spread.rolling(50).std()

    stock_data_df['z_score'] = smooth_zscore(stock_data_df['spread'])

    # Trading Signal
    stock_data_df['signal'] = stock_data_df.apply(classify_zscore, axis=1)

    return stock_data_df


def adf_test(stock_1, stock_2):
    removed_na_df = collect_metrics_for_pair(stock_1, stock_2).dropna()
    adf_result = adfuller(removed_na_df['spread'])[1]

    if adf_result <= 0.05:
        return True
    else:
        return False


@timeit
def run_adf_on_best_pairs(highest_corr_pairs):
    # Running ADF test
    adf_list = []
    m = len(highest_corr_pairs)

    print_progress_bar(0, total=m, length=50)

    for n in range(len(highest_corr_pairs)):
        result = adf_test(highest_corr_pairs['Stock_1'][n], highest_corr_pairs['Stock_2'][n])
        adf_list.append(result)

        time.sleep(0.1)
        print_progress_bar(iteration=n + 1, total=m, length=50)

    return adf_list
