import pandas as pd
import datetime as dt

# Sample DataFrame
data = {
    'Date': ['2023-01-15', '2023-01-30', '2023-02-10', '2023-02-25', '2023-03-05'],
    'Balance': [1000, 1500, 1700, 1600, 1800]
}
df = pd.DataFrame(data)

df['New Balance'] = df.apply(lambda row: row['Balance']*2, axis=1)

print(df)


# Sample DataFrame
data = {
    'Date': ['2023-01-15', '2023-01-30', '2023-02-10', '2023-02-25', '2023-03-05'],
    'Balance': [1000, 1500, 1700, 1600, 1800]
}
df = pd.DataFrame(data)





"""
@app.route('/')
def display_results():
    return render_template('results.html', table=df.to_html())

if __name__ == '__main__':
    app.run(debug=True)
"""

"""
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Resample to get the last entry of each month
monthly_df = df.resample('M').last()

# Compute the monthly differences
monthly_differences = monthly_df.diff()

print(monthly_differences)


df.loc["2023-05-02", 'GOOGL'] = 1000
df.loc["2023-07-02", 'GOOGL'] = 2000
print(df)
try:
    print(df.loc["2023-09-02", 'APPL'])
except Exception as e:
    print("Not found!")
print('GOOGL' in df.columns)




#print(p.index['GOOGL'])
print()
print()


data = {
    'date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02', '2023-01-03', '2023-01-03'],
    'name': ['Alice', 'Bob', 'Alice', 'Bob', 'Alice', 'Bob'],
    'balance': [100, 150, 200, 250, 300, 350]
}
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

print("df = ")
print(df)

# Calculate cumulative sum for each name
df['cumulative_sum'] = df.groupby('name')['balance'].cumsum()

# Pivot the DataFrame to get the desired format
cumulative_df = df.pivot_table(index='date', columns='name', values='cumulative_sum', fill_value=0)

# Reset index to get 'date' as a column
cumulative_df.reset_index(inplace=True)

print(cumulative_df)

"""



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

 # if multiple trades happened on the weekend and monday
        
           
"""
        cur_value = 0
        try:
            cur_value = values.loc[price_date, ticker] 
            cur_value = cur_value if type(cur_value) == float else 0
        except Exception as e:
            pass
            

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Portfolio Analysis</title>
    </head>
    <body>
        <h1>Portfolio Analysis</h1>
        <h2>Submission by Maya Gusak</h2>
        <h3><i>11.06.2024</i></h3>
        {{ table | safe }}
    </body>
</html>
"""
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


import ssl
import urllib.request

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://www.google.com'
try:
    response = urllib.request.urlopen(url, context=ctx)
    print("SSL module is working!")
except Exception as e:
    print("Error:", e)