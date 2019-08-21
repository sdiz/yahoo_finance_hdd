import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from yahoo_finance_hdd import YahooFinance, Parameters

class TestYahooFinance(unittest.TestCase):

    def setUp(self):
        self.params = Parameters(
            start = '2010-12-01',
            end = '2010-12-04',
            tickers = ['AAPL'],
            interval = 'd',
            exchange = 'NYSE',
            columns = ['Close']
        )

        self.yf = YahooFinance()

    def test_price_data(self):

        historical_data_df = self.yf.get_history(self.params)

        expected_data = [['2010-12-01', 45.200001], ['2010-12-02', 45.450001], ['2010-12-03', 45.348572]]

        # Create the pandas DataFrame
        expected_data_df = pd.DataFrame(expected_data, columns = ['Date', 'Close_AAPL'])
        expected_data_df = expected_data_df.set_index('Date')

        assert_frame_equal(historical_data_df, expected_data_df)


if __name__ == '__main__':
    unittest.main()