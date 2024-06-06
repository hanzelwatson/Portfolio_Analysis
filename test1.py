
import pandas as pd
import datetime as dt
from flask import Flask, render_template, request, jsonify

# Sample DataFrame
data = {
    'Date': ['2023-01-15', '2023-01-30', '2023-02-10', '2023-02-25', '2023-03-05'],
    'Balance': [1000, 1500, 1700, 1600, 1800]
}
df = pd.DataFrame(data)

app = Flask(__name__)



# Initialize the variable
variable_value = 50

@app.route('/')
def display_results():
    return render_template('index.html', variable_value=variable_value)

@app.route('/update_value', methods=['POST'])
def update_value():
    global variable_value
    variable_value = request.json.get('value')
    return jsonify(variable_value=variable_value)

if __name__ == '__main__':
    app.run(debug=True)



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