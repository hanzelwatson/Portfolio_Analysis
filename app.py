
from flask import Flask, redirect, render_template, request, jsonify
import subprocess
import stats


app = Flask(__name__)


# Initialize the confidence level and VaR
conf_level = 95
monthly_var = stats.monthly_pct_change.quantile(1 - 0.01 * conf_level).round(5)

# Initialize the risk free rate and sharpe ratio
risk_free_rate = 1
sharpe_ratio = ((stats.monthly_pct_change.mean() - 0.01 * risk_free_rate) / stats.monthly_pct_change.std()).round(5)


# Render the webpage
@app.route('/')
def display_results():


    # Define the style function for the returns tables (red: negative, green: positive)
    def color(val):
        color = 'black' 
        if val > 0:
            color = "green"
        elif val < 0:
            color = 'red'
        return f'color: {color}'


    # Apply style to the DataFrame of monthly returns (%)
    styled_returns = stats.monthly_pct_change.to_frame().round(5)
    styled_returns.reset_index(inplace=True)
    styled_returns['Date'] = styled_returns['Date'].dt.date
    styled_returns = styled_returns.set_index('Date', drop=True).style.map(color).format({'Monthly Returns %': '{:.5f}'}).set_table_styles(
        [{'selector': 'th', 'props': [('border', '1px solid black')]},
         {'selector': 'td', 'props': [('border', '1px solid black')]}]
    ).to_html()
    
    # Apply style to the DataFrame of annual returns (%)
    annual_styled_returns = stats.annual_pct_change.to_frame().round(5)
    annual_styled_returns.reset_index(inplace=True)
    annual_styled_returns['Date'] = annual_styled_returns['Date'].dt.date
    annual_styled_returns = annual_styled_returns.set_index('Date', drop=True).style.map(color).format({'Annual Returns %': '{:.5f}'}).set_table_styles(
        [{'selector': 'th', 'props': [('border', '1px solid black')]},
         {'selector': 'td', 'props': [('border', '1px solid black')]}]
    ).to_html()

    # Apply style to the DataFrame of monthly returns (USD)
    styled_returns_usd = stats.monthly_differences.to_frame().round(2)
    styled_returns_usd.reset_index(inplace=True)
    styled_returns_usd['Date'] = styled_returns_usd['Date'].dt.date
    styled_returns_usd = styled_returns_usd.set_index('Date', drop=True).style.map(color).format({'Monthly Returns USD': '{:.2f}'}).set_table_styles(
        [{'selector': 'th', 'props': [('border', '1px solid black')]},
         {'selector': 'td', 'props': [('border', '1px solid black')]}]
    ).to_html()

    # Apply style to the DataFrame of annual returns (USD)
    annual_styled_returns_usd = stats.annual_differences.to_frame().round(2)
    annual_styled_returns_usd.reset_index(inplace=True)
    annual_styled_returns_usd['Date'] = annual_styled_returns_usd['Date'].dt.date
    annual_styled_returns_usd = annual_styled_returns_usd.set_index('Date', drop=True).style.map(color).format({'Annual Returns USD': '{:.2f}'}).set_table_styles(
        [{'selector': 'th', 'props': [('border', '1px solid black')]},
         {'selector': 'td', 'props': [('border', '1px solid black')]}]
    ).to_html()
    

    return render_template('index.html', monthly_positions=stats.monthly.to_frame().to_html(),
                           monthly_differences=styled_returns_usd, 
                           monthly_pct_change=styled_returns, 
                           monthly_std=stats.monthly_pct_change.std().round(5), conf_level=conf_level, monthly_var=monthly_var,
                           max_drawdown_monthly=stats.max_drawdown_monthly.round(5), sortino_ratio_monthly=stats.sortino_ratio_monthly.round(5),
                           risk_free_rate=risk_free_rate, sharpe_ratio=sharpe_ratio,
                           annual_positions=stats.annual.to_frame().to_html(),
                           annual_differences=annual_styled_returns_usd, 
                           annual_pct_change=annual_styled_returns, 
                           annual_std=stats.annual_pct_change.std().round(5))


# Recompute the VaR given the updated confidence level from the first slider
@app.route('/update_value', methods=['POST'])
def update_value():
    global conf_level
    global monthly_var
    conf_level = int(request.json.get('value'))
    monthly_var = stats.monthly_pct_change.quantile(1 - 0.01 * conf_level).round(5)
    return jsonify(conf_level=conf_level, monthly_var=monthly_var)

# Recompute the Sharpe Ratio given the updated risk-free rate from the second slider
@app.route('/update_rate', methods=['POST'])
def update_rate():
    global risk_free_rate
    global sharpe_ratio
    risk_free_rate = int(request.json.get('rate'))
    sharpe_ratio = ((stats.monthly_pct_change.mean() - 0.01 * risk_free_rate) / stats.monthly_pct_change.std()).round(5)
    return jsonify(risk_free_rate=risk_free_rate, sharpe_ratio=sharpe_ratio)

# Jupyter Notebook displaying the data and various functions / graphs
NOTEBOOK_PATH = "Notebook.ipynb"

# Start the Jupyter Notebook (on button click)
@app.route('/start_notebook', methods=['POST'])
def start_notebook():
    # Command to start Jupyter notebook
    command = f"jupyter notebook {NOTEBOOK_PATH}"
    subprocess.Popen(command, shell=True)
    return jsonify({"status": "Notebook started"})


# Run app.py to start the web application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

