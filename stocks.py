from alpha_vantage.timeseries import TimeSeries
import pandas as pd
pd.options.plotting.backend = 'plotly'
import plotly
import os

def output_historical(ticker):
    ts = TimeSeries(os.environ["ALPHA_VANTAGE_KEY"], output_format = 'pandas')
    try:
        data, metadata = ts.get_monthly_adjusted(symbol = ticker)
        fig = data['4. close'].plot()
        fig.write_html(f'./static/stocks/{ticker}.html')
        return True
    except:
        return False