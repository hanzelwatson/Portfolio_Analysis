import pandas as pd
import datetime as dt

# Read the transaction data
transactions = pd.read_csv('tx_etf.csv', parse_dates = ['date'])
prices = pd.read_csv('px_etf.csv', parse_dates=['Date']).set_index('Date', drop = False)


# Initialize positions dictionary
# positions = {}

# tx = transactions.set_index("date", drop = False)

tx = transactions.iloc[0:52, 0:4]
first_date = pd.to_datetime(tx.index[0])
null_date = first_date + dt.timedelta(days=-1)
null_tx = pd.DataFrame({'date': null_date, 'ticker': prices.columns, 'qty': 0, 'order': 'BUY'})
print("null_tx is ")
print(null_tx)
print("concatenated...")
print(pd.concat([null_tx, tx], ignore_index=True))


# print(tx)

#for row in tx.iterrows():
#    print(row[1]['date'])

#print(tx['date'])

"""
def previous_non_empty_date(df, ticker):
    # Check if the ticker column exists in the DataFrame
    if ticker not in df.columns:
        return None

    # Get the column for the specified state
    ticker_col = df[ticker]

    # Find the first non-NaN value in the column
    first_valid_index = None
    for i in range(len(ticker_col)):
        if ticker_col[len(ticker_col) - i - 1] != None:
            return df.iloc[len(ticker_col) - i - 1, 0]
        
    return first_valid_index
"""
# could just add the date before to be all zeroes
# would be nice to collect based on the first day
positions = pd.DataFrame()
tx_first = tx.iloc[0:13]
tx_rest = tx.iloc[13:]
#print(tx_first)
#print(tx_rest)



for row in tx_first.iterrows():
    date = row[1]['date']
    ticker = row[1]['ticker']
    qty = row[1]['qty']
    order = row[1]['order']

    if order == 'BUY':
        positions.loc[date, ticker] = qty
    elif order == 'SELL':
        positions.loc[date, ticker] = -qty

prev_date = tx_first['date'][0]

#print(prev_date)

#print()
#print(tx_rest.iloc[0].loc['date'])

# Process transactions
# Assuming: all dates in tx.csv and px.csv are in chronological order and the same


# change to intertuples - returns (row_index, row_name)
for i in range(len(tx_rest)):
# for index_row in tx_rest.itertuples(): -> this returns a Pandas object
    row = tx_rest.iloc[i]
    date = row.loc['date']
    ticker = row.loc['ticker']
    qty = row.loc['qty']
    order = row.loc['order']
    
    # new problem: what if not consistent with dates?
    # I want positions to be a 2D DataFrame dates x ticker and access the one above
    """
    prev_position = positions.get((date - dt.timedelta(7), ticker))
    if order == 'BUY':
        positions[(date, ticker)] = qty + 0 if prev_position == None else prev_position 
    elif order == 'SELL':
        positions[(date, ticker)] = - qty + 0 if prev_position == None else prev_position
    """

    #prev_date = previous_non_empty_date(tx, ticker) # depends on the ticker
    cur_position = positions.loc[prev_date, ticker]
    print(cur_position)
    if order == 'BUY':
        positions.loc[date, ticker] = qty + cur_position
    elif order == 'SELL':
        positions.loc[date, ticker] = -qty + cur_position
    
    if i < len(tx_rest) and tx_rest.iloc[i].loc['date'] != date:
        prev_date = date
    


#print(tx)
print(positions)

print()
print("positions.index = ", positions.index)
print("positions.columns = ", positions.columns)
print("prices.index = ", prices[0:20].index)
print("prices.columns = ", positions[0:20].columns)
print("Calculating values...")

values = pd.DataFrame()
# calculate the values
#print(positions.map(lambda val, date, stock: val * prices.loc[date].loc[stock]))
for date in positions.index:
    for ticker in positions.columns:
        print("date = ", date)
        print("ticker = ", ticker)
        # The trade may have been placed on the weekend: in that case use Monday's price
        price_date = date
        while price_date not in prices.index:
            price_date += dt.timedelta(days=1)
        

        cur_value = 0
        try:
            cur_value = values.loc[price_date, ticker] 
            cur_value = cur_value if type(cur_value) == float else 0
        except Exception as e:
            pass
        print("cur_value = ", cur_value)
        values.loc[price_date, ticker] = positions.loc[date, ticker] * prices.loc[price_date, ticker] + cur_value

# calculate the values
print(values)

# calculate the portfolio values
print(values.sum(axis=1, numeric_only=True))

# calculate the performance of the portfolio



# documentation + tests


# Dcokerize






    