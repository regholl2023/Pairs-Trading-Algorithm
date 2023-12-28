

import unittest

import numpy as np
import pandas as pd

from Analysis.StatisticalMethods import collect_metrics_for_pair
import warnings


class TestCollectMetricsForPair(unittest.TestCase):

    def setUp(self):
        self.stock_1 = 'AAPL'
        self.stock_2 = 'MSFT'
        warnings.filterwarnings("ignore")

    #  The function should download stock data for the given stock symbols.
    def test_download_stock_data(self):
        result = collect_metrics_for_pair(self.stock_1, self.stock_2)
        assert isinstance(result, pd.DataFrame)
        assert not result.empty, "DataFrame download empty: Failed to download stock data"

    #  The function should calculate the return and forward return for each stock.
    def test_calculate_return(self):
        result = collect_metrics_for_pair(self.stock_1, self.stock_2)
        # Assert 'forward_return' is a substring of one of the column names
        assert any('forward_return' in column for column in result.columns), "forward_return not found in columns"
        # Assert 'return' is a substring of one of the column names
        assert any('return' in column for column in result.columns), "return not found in columns"


    #  The function should calculate the hedge ratio using a rolling OLS regression.
    def test_calculate_hedge_ratio(self):
        result = collect_metrics_for_pair(self.stock_1, self.stock_2)
        assert 'hedge_ratio' in result.columns, "hedge_ratio not found in columns"


    #  The function should handle cases where the downloaded stock data has missing values.
    def test_missing_stock_data(self):
        result = collect_metrics_for_pair(self.stock_1, self.stock_2)
        assert isinstance(result, pd.DataFrame), "result is not a DataFrame"
        assert not result.isnull().values.any(), "result contains NaN values"

    #  The function should handle cases where the calculated hedge ratio is infinite or NaN.
    def test_infinite_hedge_ratio(self):
        result = collect_metrics_for_pair(self.stock_1, self.stock_2)
        assert isinstance(result, pd.DataFrame), "result is not a DataFrame"
        assert not result.isin([np.inf, -np.inf, np.nan]).values.any(), "result contains infinite or NaN values"

    #  The function should calculate the spread of stock 1 and stock 2 price.
    def test_calculate_spread(self):
        result = collect_metrics_for_pair(self.stock_1, self.stock_2)
        assert isinstance(result, pd.DataFrame), "result is not a DataFrame"
        assert 'spread' in result.columns, "spread not found in columns"

    #  The function should calculate the rolling correlation test.
    def test_calculate_rolling_correlation(self):
        result = collect_metrics_for_pair(self.stock_1, self.stock_2)
        assert isinstance(result, pd.DataFrame), "result is not a DataFrame"
        assert 'roll_corr' in result.columns, "roll_corr not found in columns"

    #  The function should calculate the z-score.
    def test_calculate_z_score(self):
        result = collect_metrics_for_pair(self.stock_1, self.stock_2)
        assert isinstance(result, pd.DataFrame), "result is not a DataFrame"
        assert 'z_score' in result.columns, "z_score not found in columns"
