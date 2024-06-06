import pandas as pd
import datetime as dt
import numpy as np

print("Portfolio Analysis")
print("Submission by Maya Gusak")
print("11.06.2024")
print()
print()

# Read the transaction data
transactions = pd.read_csv('tx_etf.csv', parse_dates=['date']).set_index('date', drop=True)
prices = pd.read_csv('px_etf.csv', parse_dates=['Date']).set_index('Date', drop=True)

tx = transactions.iloc[0:700]
pd.to_datetime(tx.index)

# Add a column that equals qty if order=BUY and -qty if order=SELL
tx['adjusted_qty'] = tx.apply(lambda row: row['qty'] if row['order'] == 'BUY' else -row['qty'], axis=1)

print("Read from file: transactions")
print(tx.head())
print()

# Calculate the cumulative sum of the signed qty column to get the position
tx['positions'] = (tx.groupby('ticker'))['adjusted_qty'].cumsum()


# Pivot the DataFrame to get the desired format
positions = tx.pivot_table(index='date', columns='ticker', values='positions', fill_value=0)

# Reset index to get 'date' as a column
positions.reset_index(inplace=False)


print("Reconstructed portfolio positions...")
print(positions.head())
print()
# monthly and yearly portfolio compositions
print("Monthly positions...")
print(positions.resample('ME').last())
print()
print("Annual positions...")
print(positions.resample('YE').last())
print()
print()



# Make a new Data Frame to compute the values in the portfolio
# The trade order may have been placed on the weekend: in that case use Monday's price
# Assumption: Only one order per ETF is placed per week... otherwisecompute the cumulative sum over weekend dates 
values = pd.DataFrame()
for date in positions.index:
    for ticker in positions.columns:
        
        
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

        

print("Portfolio values for each ETF...")
print(values.head())
print()

# Calculate the portfolio values
portfolio = values.sum(axis=1, numeric_only=True)
print("Portfolio values...")
print(portfolio.head())
print()

# Calculate the portfolio monthly performance
# Resample to get the last entry of each month and compute the monthly differences / returns
monthly = portfolio.resample('ME').last().rename_axis("Date").rename("Monthly Value")
monthly_differences = monthly.diff().iloc[1:].dropna().rename_axis("Date").rename("Monthly Returns USD")
monthly_pct_change = monthly.pct_change().iloc[1:].dropna().rename_axis("Date").rename("Monthly Returns %")

print("Monthly Analysis:")
print()
print()
print("Monthly values...")
print(monthly)
print()
print("Monthly returns (USD)...")
print(monthly_differences)
print()
print("Monthly returns (%)...")
print(monthly_pct_change)
print()
print()

# Calculate the portfolio annual performance
# Resample to get the last entry of each year and compute the annual differences / returns
annual = portfolio.resample('YE').last().rename_axis("Date").rename("Value")
annual_differences = annual.diff().iloc[1:].dropna().rename_axis("Date").rename("Annual Returns USD")
annual_pct_change = annual.pct_change().iloc[1:].dropna().rename_axis("Date").rename("Annual Returns %")

print("Annual Analysis:")
print()
print()
print("Annual values...")
print(annual)
print()
print("Annual returns (USD)...")
print(annual_differences)
print()
print("Annual returns (%)...")
print(annual_pct_change)
print()
print()


print("Risk measures:")
print()

# Compute the volatility
print("Monthly volatility: ", monthly_pct_change.std())
print("Annual volatility: ", annual_pct_change.std())
print()

# Compute the Value at Risk (VaR)
confidence_level = 0.95
print("Monthly 95% VaR: ", monthly_pct_change.quantile(1 - confidence_level))
print("Annual 95% VaR: ", annual_pct_change.quantile(1 - confidence_level))
print()

# Sharpe Ratio: measures the risk-adjusted return
risk_free_rate = 0.01  # Example risk-free rate
print("Monthly Sharpe Ratio 1% risk free rate: ", (monthly_pct_change.mean() - risk_free_rate) / monthly_pct_change.std())
print("Annual Sharpe Ratio 1% risk free rate: ", (annual_pct_change.mean() - risk_free_rate) / annual_pct_change.std())
print()
print()

print("More monthly risk measures...")
print()

# Sortino Ratio: similar to the Sharpe Ratio, but only considers downside risk
downside_returns = monthly_pct_change.loc[lambda x: x < 0]
sortino_ratio = (monthly_pct_change.mean() - risk_free_rate) / downside_returns.std()
print("Sortino ratio (sampled monthly): ", sortino_ratio)
print()

# Maximum drawdown: the largest peak-to-trough decline in the portfolio value.
cumulative_returns = (1 + monthly_pct_change).cumprod()
peak = cumulative_returns.cummax()
drawdown = (cumulative_returns - peak) / peak
max_drawdown = drawdown.min()
print("Max drawdown (sampled monthly): ", max_drawdown)


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

    
