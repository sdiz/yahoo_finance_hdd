"""
Download historical financial data from yahoo finance

@author: Serkan Dizbay

# ********************************
# EXAMPLE
# ********************************

# create parameter object
params = Parameters(
            start = '2010-12-01',
            end = '2019-08-20',
            tickers = ['AAPL', 'VZ', 'JPM'],
            interval = 'w',
            exchange = 'NYSE',
            columns = ['Open', 'Close']
        )

# e.g set interval to daily
params.interval = 'd'

# create new yahoo finance instance
yf = YahooFinance()

# download historical financial price data
df1 = yf.get_history(params)

# download historical dividends data
df2 = yf.get_dividends(params)

# download historical stock splits data
df3 = yf.get_splits(params)

# export dataframe to excel
df1.to_excel('C:/Users/username/Desktop/data.xlsx')

"""

########################
# IMPORTS
########################
import numpy as np
import pandas as pd
import requests
import re
import itertools
from multiprocessing.dummy import Pool as ThreadPool
from io import StringIO
from datetime import datetime
from time import mktime
from yahoo_finance_hdd.exchange_calendars import ExchangeCalendar


class Connection:
    """
    Abstract base class specifying methods to be implemented
    by session class.
    """

    def get_session(self):
        raise NotImplementedError

    def get_crumb(self):
        raise NotImplementedError

class Parameters:
    """
    A class for defining all the parameters used for downloading
    historical financial data from yahoo finance.

    ...

    Attributes
    ----------
    start : str
        the start date of the data series ('yyyy-mm-dd').
    end : str
        the end date of the data series ('yyyy-mm-dd').
    tickers : str || list
        single tickers can be passed as a string. Multiple tickers
        have to be passed as a list e.g ['IBM', 'AAPL'].
    interval : str
        specify the frequency of the data series.
        'd' = daily
        'w' = weekly
        'm' = monthly
    exchange : str
        the exchange to obtain the dates for the data series (default NYSE)
        available exchanges are:
            ['BMF', 'CFE', 'CME', 'CBOT', 'COMEX', 'NYMEX', 'EUREX', 'ICE', 'ICEUS', 'NYFE', 'JPX', 'LSE', 'NYSE',
            'stock', 'NASDAQ', 'BATS', 'OSE', 'SIX', 'TSX', 'TSXV', 'SSE', 'HKEX']
    columns : list
        a list of strings specifying the data columns to be returned.
        Allowed columns are 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'.
    """

    def __init__(self, start, end, tickers, interval, exchange, columns):
        self.start = start
        self.end = end
        self.tickers = tickers
        self.interval = interval
        self.exchange = exchange
        self.columns = columns

class Session(Connection):
    """
    A class which is used to create a new yahoo finance session.

    ...

    Attributes
    ----------
    CRUM_STR : str
        the url to fetch the crumb from
    session : Session
        a session object which allows persistent parameters across requests
    crumb : str
        an alphanumeric code which is used when making requests
    """

    CRUM_STR = 'https://finance.yahoo.com/quote/SPY/history?p=SPY'

    def __init__(self):
        self.session = requests.Session()
        self.crumb = self._get_crumb()

        # check if wrong crumb fetched which leads to unauthorized 401 error
        while "\\" in self.crumb:
            self.session = requests.Session()
            self.crumb = self._get_crumb()

    def _get_crumb(self):
        """
        Fetch crumb from yahoo finance

        Returns
        -------
        str
           an alphanumeric code which is used when making requests
        """
        self.response = self.session.get(self.CRUM_STR)
        self.response.raise_for_status()
        self.message = re.search(r'CrumbStore":{"crumb":"(.*?)"}', self.response.text)

        if not self.message:
            raise ValueError('Could not get crumb from Yahoo Finance')
        else:
            return self.message.group(1)

    def get_session(self):
        """ Get session object """
        return self.session

    def get_crumb(self):
        """ Get crumb associated with created session"""
        return self.crumb


class Download:
    """
    A class which is used to download historical data from yahoo finance.

    ...

    Attributes
    ----------
    URL_STR : str
        the url to fetch the data from
    session : object
        session object used for making http requests
    crumb : str
        an alphanumeric code which is used when making requests
    params : object
        all the parameters used when downloading data
    """

    URL_STR = "https://query1.finance.yahoo.com/v7/finance/download/%s"
    URL_STR += "?period1=%s&period2=%s&interval=%s&events=%s&crumb=%s"

    def __init__(self, conn: Connection, params: Parameters):
        self.session = conn.get_session()
        self.crumb = conn.get_crumb()
        self.params = params

    def _get_url(self, url):
        """
        Scrape data from provided url.

        Parameters
        ----------
        url : str
            the url to get the data from

        Returns
        -------
        pandas.DataFrame
            the fetched data
        """

        self.response = self.session.get(url)
        self.response.raise_for_status()

        return pd.read_csv(StringIO(self.response.text), error_bad_lines=False).replace('null', np.nan).dropna()

    def _download_thread(self, identifier):
        """
        Download data series in thread.

        Parameters
        ----------
        identifier : str
            specify what kind of financial data to download.
            'history' = price data
            'div' = dividend data
            'split' = stock split data

        Returns
        -------
        pandas.DataFrame
            the financial data series
        """

        # a pool of workers
        self.pool = ThreadPool(4)

        # get data for each ticker in thread and return results
        self.results = self.pool.starmap(self._get_single_ticker, zip(self.params.tickers, itertools.repeat(identifier)))

        # close the pool and wait for threads to finish
        self.pool.close()
        self.pool.join()

        return self.results

    def _get_single_ticker(self, ticker, identifier):
        """
        Download data series for single ticker.

        Parameters
        ----------
        ticker : str
            the name of the ticker e.g 'AAPL'
        identifier : str
            specify what kind of financial data to download.
            'history' = price data
            'div' = dividend data
            'split' = stock split data

        Returns
        -------
        pandas.DataFrame
            the financial data series
        """

        # convert dates to unix
        self.start_unix = Date.convert_to_unix(self.params.start)
        self.end_unix = Date.convert_to_unix(self.params.end)

        # get data
        self.output = self._get_url(self.URL_STR % (ticker, self.start_unix, self.end_unix, '1d', identifier, self.crumb))

        # set name of index column to ticker name
        self.output.index.name = ticker

        return self.output

    def get_multiple_tickers(self, identifier):
        """
        Download data for multiple tickers. The data is retrieved individually in threads for each
        ticker and merged at the end to get a consistent data series.

        Parameters
        ----------
        identifier : str
            specify what kind of financial data to download.
            'history' = price data
            'div' = dividend data
            'split' = stock split data

        Returns
        -------
        pandas.DataFrame
            the merged data series
        """

        # add date column to columns list
        if 'Date' not in self.params.columns:
            self.params.columns.insert(0, 'Date')

        # transform tickers
        self.tickers = Tickers.transform(self.params.tickers)

        # get dates from trading calendar
        self.output_df = ExchangeCalendar(self.params.start, self.params.end, self.params.exchange).get_dates(self.params.interval)

       # get data for each ticker in thread and return results
        self.results = self._download_thread(identifier)

        # merge dataframes
        for result in self.results:

            if identifier == 'history':
                self.data_df = result[self.params.columns]
            else:
                self.data_df = result

            # rename columns
            for column in self.data_df.columns:
                if column != 'Date':
                    self.data_df = self.data_df.rename(columns={column: column + "_" + self.data_df.index.name})

            # merge data series with dates
            self.output_df = pd.merge(self.output_df, self.data_df, how='left', on='Date')

        # make date column index
        self.output_df = self.output_df.set_index('Date')

        return self.output_df.dropna(how='all')



class Tickers:

    @staticmethod
    def transform(tickers):
        """
        Convert tickers to list of uppercase strings.

        Parameters
        ----------
        tickers : str || list
            single tickers can be passed as a string. Multiple tickers
            have to be passed as a list e.g ['IBM', 'AAPL'].

        Returns
        -------
        list
            a list of uppercase strings
        """

        ticker_list = tickers if isinstance(tickers, list) else [tickers]
        return [elem.upper() for elem in ticker_list]


class Date:

    @staticmethod
    def convert_to_unix(date):
        """
        Convert string date to unix.

        Parameters
        ----------
        date : str
            the date ('yyyy-mm-dd').

        Returns
        -------
        int
            unix value
        """

        unixdate = datetime.strptime(date, '%Y-%m-%d')
        return int(mktime(unixdate.timetuple()))



class YahooFinance:
    """
    This class provides easy to use methods to
    download historical financial data from yahoo finance.
    """

    # create new session
    session = Session()

    def get_history(self, params: Parameters):
        """
        Download historical financial data from yahoo finance.

        Parameters
        ----------
        params : object
            parameters object with all the parameters
            used when downloading data

        Returns
        -------
        pandas.DataFrame
            the financial data series
        """

        return Download(self.session, params).get_multiple_tickers('history')

    def get_dividends(self, params: Parameters):
        """
        Download historical dividend data from yahoo finance.

        Parameters
        ----------
        params : object
            parameters object with all the parameters
            used when downloading data

        Returns
        -------
        pandas.DataFrame
            the financial data series
        """

        return Download(self.session, params).get_multiple_tickers('div')

    def get_splits(self, params: Parameters):
        """
        Download historical data for stock splits from yahoo finance.

        Parameters
        ----------
        params : object
            parameters object with all the parameters
            used when downloading data

        Returns
        -------
        pandas.DataFrame
            the financial data series
        """

        return Download(self.session, params).get_multiple_tickers('split')
