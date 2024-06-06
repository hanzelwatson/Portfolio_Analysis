import pandas as pd
import datetime as dt
import numpy as np

# Read the transaction data
transactions = pd.read_csv('tx_etf.csv', parse_dates=['date']).set_index('date', drop=True)
prices = pd.read_csv('px_etf.csv', parse_dates=['Date']).set_index('Date', drop=True)


tx = transactions.iloc[0:700]
pd.to_datetime(tx.index)

tx['adjusted_qty'] = tx.apply(lambda row: row['qty'] if row['order'] == 'BUY' else -row['qty'], axis=1)

print(tx.head())

# Calculate cumulative sum for each name
tx['positions'] = (tx.groupby('ticker'))['adjusted_qty'].cumsum()

print(tx.head())

# Pivot the DataFrame to get the desired format
positions = tx.pivot_table(index='date', columns='ticker', values='positions', fill_value=0)

# Reset index to get 'date' as a column
positions.reset_index(inplace=False)

print(positions.head())


values = pd.DataFrame()



for date in positions.index:
    for ticker in positions.columns:
        # The trade may have been placed on the weekend: in that case use Monday's price
        
        price_date = date
        while price_date not in prices.index:
            price_date += dt.timedelta(days=1)
        
        # if multiple trades happened on the weekend and monday
        """
        cur_value = 0
        try:
            cur_value = values.loc[price_date, ticker] 
            cur_value = cur_value if type(cur_value) == float else 0
        except Exception as e:
            pass
        """
        
        values.loc[price_date, ticker] = positions.loc[date, ticker] * prices.loc[price_date, ticker] # + cur_value

        


# any way to print values without making a new data frame?

# calculate the values
print(values.head())

# calculate the portfolio values
portfolio = values.sum(axis=1, numeric_only=True)
print(portfolio.head())

# calculate the performance
# Resample to get the last entry of each month
monthly = portfolio.resample('ME').last()
print(monthly.head())

# Compute the monthly differences
monthly_differences = monthly.diff().iloc[1:].dropna()
monthly_pct_change = monthly.pct_change().iloc[1:].dropna()
print(monthly_pct_change)
# Assuming that we start off with an empty portfolio
# monthly_differences.iloc[0] = monthly.iloc[0]

annually = portfolio.resample('YE').last()
print(annually)




# Compute the annual differences
annually_differences = annually.diff().iloc[1:].dropna()
annually_pct_change = annually.pct_change().iloc[1:].dropna()
# Assuming that we start off with an empty portfolio
# annually_differences.iloc[0] = annually.iloc[0]

print(annually_differences)
print(annually_pct_change)



# monthly and yearly portfolio compositions
print(positions.resample('ME').last())
print(positions.resample('YE').last())

# volatility
print(monthly_pct_change.std())
print(annually_pct_change.std())

# Value at Risk (VaR)
# Calculate Value at Risk (VaR)
confidence_level = 0.95
print(monthly_pct_change.quantile(1 - confidence_level))
print(annually_pct_change.quantile(1 - confidence_level))

# Sharpe Ratio: measures the risk-adjusted return
risk_free_rate = 0.01  # Example risk-free rate
print((monthly_pct_change.mean() - risk_free_rate) / monthly_pct_change.std())
print((annually_pct_change.mean() - risk_free_rate) / annually_pct_change.std())

# Maximum drawdown: the largest peak-to-trough decline in the portfolio value.
cumulative_returns = (1 + monthly_pct_change).cumprod()
peak = cumulative_returns.cummax()
drawdown = (cumulative_returns - peak) / peak
max_drawdown = drawdown.min()
print("max_drawdown = ", max_drawdown)

# Sortino Ratio: similar to the Sharpe Ratio, but only considers downside risk
downside_returns = monthly_pct_change.loc[lambda x: x < 0]
sortino_ratio = (monthly_pct_change.mean() - risk_free_rate) / downside_returns.std()
print("sortino_ratio = ", sortino_ratio)

# need to give the monthly/annually_pct_change (aka the "returns") labels




"""
null_date = pd.to_datetime(tx.index[0]) + dt.timedelta(days=-1)

positions_data = {'date': [null_date]} 
for ticker in prices.columns:
    positions_data[ticker] = [0]
print("positions_data: ")
print(positions_data)

positions = pd.DataFrame(positions_data)
positions['date'] = pd.to_datetime(positions['date'])
positions.set_index('date', inplace=True, drop=True)

print(positions)

prev_date = null_date
for i in range(len(tx)):
    row = tx.iloc[i]
    date = row.loc['date']
    ticker = row.loc['ticker']
    qty = row.loc['qty']
    order = row.loc['order']

    cur_position = positions.loc[prev_date, ticker]
    if order == 'BUY':
        positions.loc[date, ticker] = qty + cur_position
    elif order == 'SELL':
        positions.loc[date, ticker] = -qty + cur_position
    
    if i < len(tx) - 1 and tx.iloc[i+1].loc['date'] != date:
        prev_date = date

positions.drop(index=null_date)
print(positions)


# calculate the performance of the portfolio
"""

# Tomorrow:


# documentation + tests!


# Dockerize


# Then create a Jupyter notebook for this stuff and also figure that out. (does this go in the container?)


# See if we can make a web server and put some graphs on there (and containerize it)


# Make sure to include a README!

    
