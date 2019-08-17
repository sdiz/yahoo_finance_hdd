from yahoo_finance_hdd import YahooFinance, Parameters

# create parameter object
params = Parameters(
            start = '2010-12-01',
            end = '2019-08-20',
            tickers = ['AAPL', 'VZ', 'JPM'],
            interval = 'w',
            exchange = 'NYSE',
            columns = ['Close', 'Adj Close']
        )

# e.g change interval to daily
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
#df1.to_excel('C:/Users/username/Desktop/data.xlsx')