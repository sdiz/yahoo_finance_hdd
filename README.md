# Yahoo Finance Historical Data Downloader

Download historical price, dividends and stock splits data from yahoo finance in python.

- Current Version: v_0.2.1
- Version Released: 2019-08-17
- Report any bugs by opening an issue here: https://github.com/sdiz/yahoo_finance_hdd/issues

## Installation

  - This module runs on python >= 3.3. It might run on other version, but has not been tested.
  - Dependencies: numpy, pandas, requests, pandas_market_calendars.
          
1. Installation using pip:
    ```bash
    $ pip install yahoo_finance_hdd
    ```
1. Installation using github:
    ```bash
    $ git clone https://github.com/sdiz/yahoo_finance_hdd.git
    $ cd yahoo_finance_hdd
    $ python setup.py install
    ```
## Usage

- The data from all methods is returned as a pandas dataframe.
- Create a parameters object to define all necessary input parameters
    - start :  the start date of the data series ('yyyy-mm-dd').
    - end : the end date of the data series ('yyyy-mm-dd').
    - tickers : single tickers can be passed as a string. Multiple tickers
                have to be passed as a list e.g ['IBM', 'AAPL'].
    - interval : specify the frequency of the data series.
        - 'd' = daily
        - 'w' = weekly
        - 'm' = monthly
    - exchange : the exchange to obtain the dates for the data series (default NYSE)
        - available exchanges are: ['BMF', 'CFE', 'CME', 'CBOT', 'COMEX', 'NYMEX', 'EUREX', 'ICE', 'ICEUS', 'NYFE', 'JPX', 'LSE', 'NYSE', 'stock', 'NASDAQ', 'BATS', 'OSE', 'SIX', 'TSX', 'TSXV', 'SSE', 'HKEX']
    - columns : a list of strings specifying the data columns to be returned.
        - ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
-   Available methods
    - get_history(params) : download historical financial price data from yahoo finance.
    - get_dividends(params) : download historical dividend data from yahoo finance.
    - get_splits(params) : download historical data for stock splits from yahoo finance.


## Examples

```python
from yahoo_finance_hdd import YahooFinance, Parameters

# create parameter object
params = Parameters(
            start = '2010-12-01',
            end = '2019-08-20',
            tickers = ['AAPL', 'VZ', 'JPM'],
            interval = 'w',
            exchange = 'NYSE',
            columns = ['Open', 'Close']
        )

# e.g change interval to daily
params.interval = 'd'

# create new yahoo finance instance
yf = YahooFinance()

# download historical financial price data
price_df = yf.get_history(params)

# download historical dividends data
dividends_df = yf.get_dividends(params)

# download historical stock splits data
splits_df = yf.get_splits(params)
```
### Returned Data
![alt text](https://github.com/sdiz/yahoo_finance_hdd/blob/master/return_example.JPG "returned data example")

## Authors

- **Serkan Dizbay** - https://github.com/sdiz

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

