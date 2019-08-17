"""
Exchange calendars for trading applications

@author: Serkan Dizbay

# ********************************
# EXAMPLE
# ********************************

# daily sequence of date values
df1 = ExchangeCalendar('2012-12-01', '2019-04-14', 'NYSE').get_dates('d')

# weekly sequence of date values
df2 = ExchangeCalendar('2012-12-01', '2019-04-14', 'NYSE').get_dates('w')

# monthly sequence of date values
df3 = ExchangeCalendar('2012-12-01', '2019-04-14', 'NYSE').get_dates('m')

"""

########################
# IMPORTS
########################
import pandas_market_calendars as tcal
import pandas as pd

class ExchangeCalendar:
    """
    A wrapper for the pandas_market_calendars package with added
    functionalities such as data frequency sampling.

    ...

    Attributes
    ----------
    start : str
        the start date ('yyyy-mm-dd').
    end : str
        the end date ('yyyy-mm-dd').
    exchange : str
        the exchange to obtain the dates for the data series (default NYSE)
        available exchanges are:
            ['BMF', 'CFE', 'CME', 'CBOT', 'COMEX', 'NYMEX', 'EUREX', 'ICE', 'ICEUS', 'NYFE', 'JPX', 'LSE', 'NYSE',
            'stock', 'NASDAQ', 'BATS', 'OSE', 'SIX', 'TSX', 'TSXV', 'SSE', 'HKEX']
    date_range : pandas.DatetimeIndex
        a range of dates
    """

    def __init__(self, start, end, exchange='NYSE'):
        self.start = start
        self.end = end
        self.exchange = exchange
        ExchangeCalendar.date_range = self.get_daterange()

    def get_daterange(self):
        """
        Generate a sequence of datetime values

        Returns
        -------
        pandas.DatetimeIndex
           a range of dates
        """

        exchange_cal = tcal.get_calendar(self.exchange)
        dates = exchange_cal.schedule(start_date=self.start, end_date=self.end)
        return tcal.date_range(dates, frequency='1D')

    def get_dates(self, time_interval):
        """
        Get a sequence of date values based on frequency input.

        Parameters
        ----------
        time_interval : str
            frequency of the time series
            allowed inputs are:
                'd' = daily
                'w' = weekly
                'm' = monthly

        Returns
        -------
        pandas.DataFrame
            the data series
        """

        if time_interval == 'd': return self.Daily().get_dates()
        if time_interval == 'w': return self.Weekly().get_dates()
        if time_interval == 'm': return self.Monthly().get_dates()
        assert time_interval in ['d', 'w', 'm'], "Invalid interval "+ str(time_interval) + "." + " Allowed inputs are ['d', 'w', 'm']"


    class Daily():

        @staticmethod
        def get_dates():
            return pd.DataFrame(data=ExchangeCalendar.date_range.strftime('%Y-%m-%d'),
                                columns={'Date'})

    class Weekly():

        @staticmethod
        def day_of_week_num(dts):
            return (dts.astype('datetime64[D]').view('int64') - 4) % 7

        def _get_weekly_dates(self, daily_dr):
            return [previous_date for current_date, previous_date in zip(daily_dr, daily_dr[1:])
                    if self.day_of_week_num(current_date) > self.day_of_week_num(previous_date)]

        def get_dates(self):
            return pd.DataFrame(data=self._get_weekly_dates
                                (ExchangeCalendar.date_range.strftime('%Y-%m-%d')),
                                columns={'Date'})

    class Monthly():

        @staticmethod
        def _get_monthly_dates(daily_dr, monthly_dr):
            return [z for x, y, z in zip(monthly_dr, monthly_dr[1:], daily_dr[1:]) if y != x]

        def get_dates(self):
            return pd.DataFrame(data=self._get_monthly_dates(
                    ExchangeCalendar.date_range.strftime('%Y-%m-%d'),
                    ExchangeCalendar.date_range.strftime('%m')),
                    columns={'Date'})
