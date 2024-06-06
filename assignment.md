Assignment - Junior Software Engineer
======================================

## Goal of the assignment

Implement a script that can calculate the value and performance of a portfolio of ETFs over time derived from a CSV file containing transaction data.

You will need to:

- reconstruct the positions from the transactions
- value the positions over time  (value = price x position)
- calculate the performance of the portfolio (in % and in USD)

### Input

The provided input is in two CSV files containing transactions and prices.

tx_etf.csv:

- `date`: the date of the position
- `ticker`: the ticker of the position
- `qty`: the quantity of the order
- `order`: BUY or SELL
- assume the trades were executed with the end-of-day prices in the px_etf.csv

px_etf.csv:

- `date`: settlement price date
- end of day prices of the ETFs (in USD, pre column)

Note: the prices in px_etf.csv are the "adjusted" prices (dividens, splits). For simplicity you can assume these are the traded settlement prices for the instruments.

## Deliverables

A runnable python script that can be executed from the command line.
The minimum required output needs to contain a performance table with Monthly and the Annual simple returns (%).
Provide any additional output that you think is relevant (e.g. the composition of the portfolio on a monthly basis or any risk measures you think are relevant).

### The ideal solution

- correctly reproduces the positions of the portfolio
- shows good structure and is easy to understand
- is well documented, well-structured and formatted
- delivered as a 'dockerized' solution (i.e the whole solution is built and runnable in a reproducible environment with all dependencies defined)

### Bonus points

- deliver a Jupyter notebook that allows to explore the data, execute functions that generate the output(s)
- implement a simple web interface to visualize the performance of the portfolio
- include charts (with a library of your choice) to visualize the performance and composition of the portfolio through time
