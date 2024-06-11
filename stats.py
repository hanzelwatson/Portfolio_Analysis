import pandas as pd
import datetime as dt


# Read the transaction data
tx = pd.read_csv('tx_etf.csv', parse_dates=['date']).set_index('date', drop=True)
prices = pd.read_csv('px_etf.csv', parse_dates=['Date']).set_index('Date', drop=True)

# tx = tx.iloc[0:700].copy() # for testing a smaller data set
pd.to_datetime(tx.index)

# Add a column that equals qty if order=BUY and -qty if order=SELL
tx['adjusted_qty'] = tx.apply(lambda row: row['qty'] if row['order'] == 'BUY' else -row['qty'], axis=1)

# Calculate the cumulative sum of the signed qty column to get the position
tx['positions'] = (tx.groupby('ticker'))['adjusted_qty'].cumsum()

# Pivot the DataFrame to get the desired format
positions = tx.pivot_table(index='date', columns='ticker', values='positions', fill_value=0)

# Reset index to get 'date' as a column
positions.reset_index(inplace=False)

# Make a new Data Frame to compute the values in the portfolio
# The trade order may have been placed on the weekend: in that case use Monday's price
# Assumption: Only one order per ETF is placed per week... 
# otherwise, compute the cumulative sum over weekend dates (omitted for simplicity)
values = pd.DataFrame()
for date in positions.index:
    for ticker in positions.columns:
        
        price_date = date
        while price_date not in prices.index:
            price_date += dt.timedelta(days=1)
        
        values.loc[price_date, ticker] = positions.loc[date, ticker] * prices.loc[price_date, ticker] # + cur_value


# Calculate the portfolio values
portfolio = values.sum(axis=1, numeric_only=True)

# Calculate the portfolio monthly performance
# Resample to get the last entry of each month and compute the monthly differences / returns
monthly = portfolio.resample('M').last().rename_axis("Date").rename("Monthly Value")
monthly_differences = monthly.diff().iloc[1:].dropna().rename_axis("Date").rename("Monthly Returns USD").round(2)
monthly_pct_change = monthly.pct_change().iloc[1:].dropna().rename_axis("Date").rename("Monthly Returns %").round(5)

# Calculate the portfolio annual performance
# Resample to get the last entry of each year and compute the annual differences / returns
annual = portfolio.resample('Y').last().rename_axis("Date").rename("Value")
annual_differences = annual.diff().iloc[1:].dropna().rename_axis("Date").rename("Annual Returns USD")
annual_pct_change = annual.pct_change().iloc[1:].dropna().rename_axis("Date").rename("Annual Returns %")

risk_free_rate = 0.01  # Example risk-free rate

# Sortino Ratio: similar to the Sharpe Ratio, but only considers downside risk
downside_monthly_returns = monthly_pct_change.loc[lambda x: x < 0]
sortino_ratio_monthly = (monthly_pct_change.mean() - risk_free_rate) / downside_monthly_returns.std()

downside_annual_returns = annual_pct_change.loc[lambda x: x < 0]
sortino_ratio_annual = (annual_pct_change.mean() - risk_free_rate) / downside_annual_returns.std()

# Maximum drawdown: the largest peak-to-trough decline in the portfolio value.
cumulative_returns = (1 + monthly_pct_change).cumprod()
peak = cumulative_returns.cummax()
drawdown = (cumulative_returns - peak) / peak
max_drawdown_monthly = drawdown.min()

cumulative_returns = (1 + annual_pct_change).cumprod()
peak = cumulative_returns.cummax()
drawdown = (cumulative_returns - peak) / peak
max_drawdown_annual = drawdown.min()


# Print output directly only when this application is run
def main():

    print("Portfolio Analysis")
    print("Submission by Maya Gusak")
    print("11.06.2024")
    print()
    print()

    print("Read from file: transactions")
    print(tx.head())
    print()

    print("Reconstructed portfolio positions...")
    print(positions.head())
    print()
    # monthly and yearly portfolio compositions
    print("Monthly positions...")
    print(positions.resample('M').last())
    print()
    print("Annual positions...")
    print(positions.resample('Y').last())
    print()
    print()


    print("Portfolio values for each ETF...")
    print(values.round(2).head())
    print()
    print("Portfolio values...")
    print(portfolio.head())
    print()
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
    print("Monthly Sharpe Ratio 1% risk free rate: ", (monthly_pct_change.mean() - risk_free_rate) / monthly_pct_change.std())
    print("Annual Sharpe Ratio 1% risk free rate: ", (annual_pct_change.mean() - risk_free_rate) / annual_pct_change.std())
    print()
    print()

    print("More risk measures...")
    print()

    print("Sortino ratio (sampled monthly): ", sortino_ratio_monthly)
    print("Sortino ratio (sampled annually): ", sortino_ratio_annual)
    print()
    print("Max drawdown (sampled monthly): ", max_drawdown_monthly)
    print("Max drawdown (sampled annually): ", max_drawdown_annual)

if __name__ == "__main__":
    main()
