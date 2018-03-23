from flask import Flask, render_template, request, redirect

import requests

import pandas as pd

import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file


app = Flask(__name__)


@app.route('/')
def home():
    '''receive user input through flask site'''
    user_input = 'AMZN'

    '''Quandl API request'''
    ticker = 'https://www.quandl.com/api/v3/datasets/WIKI/AAPL?trim_start=2016-01-01&trim_end=2018-03-05&api_key=v1eCq4j6XirYCp4gU9VJ'
    ticker = ticker.replace('AAPL', user_input)

    r = requests.get(ticker)

    #create dictionary of API call:
    d = r.json()

    #these are the columns names:
    # ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Ex-Dividend', 'Split Ratio', 'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']
    columns = d['dataset']['column_names']

    data = d['dataset']['data']

    '''create pandas df'''
    df = pd.DataFrame(data, columns=columns)


    '''create bokeh figure'''
    def datetime(x):
        return np.array(x, dtype=np.datetime64)

    p1 = figure(x_axis_type="datetime", title="Stock Closing Prices")
    p1.grid.grid_line_alpha=0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'

    p1.line(datetime(df['Date']), df['Close'], color='#A6CEE3', legend=user_input)
    p1.legend.location = "top_left"

    output_file("stocks.html", title="stocks.py example")


    return render_template('home.html')



# @app.route('/about')
# def about():
#     return render_template('about.html')

if __name__ == '__main__':
  app.run()
