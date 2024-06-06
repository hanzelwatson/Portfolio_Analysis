import pandas as pd
# from datetime import datetime

# Read the transaction data
transactions = pd.read_csv('tx_etf.csv')
prices = pd.read_csv('px_etf.csv')

# Convert date columns to datetime
# transactions['date'] = pd.to_datetime(transactions['date'])
# prices['date'] = pd.to_datetime(prices['date'])

# Initialize positions dictionary
positions = {}

# Process transactions
prev_date = 0
for row in transactions.iterrows():
    date = row[1]['date']
    ticker = row[1]['ticker']
    qty = row[1]['qty']
    order = row[1]['order']
    
    if order == 'BUY':
        positions[date, ticker] = positions.get(prev_date, ticker) + qty
    elif order == 'SELL':
        positions[date, ticker] = positions.get(prev_date, ticker) - qty
    
    prev_date = date

# Initialize portfolio value dataframe
portfolio_values = prices['date'].copy()

# Calculate daily portfolio values
for date in transactions.date():
    for ticker in positions.key():
        portfolio_values[date, ticker] = positions
for ticker in positions.keys():
    portfolio_values[date, ticker] = positions[ticker] * prices[ticker]

# Calculate total portfolio value
portfolio_values['total_value'] = portfolio_values.drop(columns=['date']).sum(axis=1)

# Calculate monthly and annual returns
portfolio_values['month'] = portfolio_values['date'].dt.to_period('M')
monthly_returns = portfolio_values.groupby('month')['total_value'].last().pct_change() * 100

portfolio_values['year'] = portfolio_values['date'].dt.to_period('Y')
annual_returns = portfolio_values.groupby('year')['total_value'].last().pct_change() * 100

# Output the performance table
performance_table = pd.DataFrame({
    'Monthly Returns (%)': monthly_returns,
    'Annual Returns (%)': annual_returns
}).dropna()

print(performance_table)

# Save output to a CSV file
performance_table.to_csv('performance_table.csv', index=False)
