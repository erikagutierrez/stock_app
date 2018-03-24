from flask import Flask, render_template, request, redirect
import os

import requests

import pandas as pd

import numpy as np
from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.embed import components

from datetime import date, timedelta
from monthdelta import monthdelta


app = Flask(__name__)

@app.route('/stock_ticker')
def stock_ticker():

    '''receive user input through flask site'''
    user_input = request.args.get('ticker').upper()
    if user_input == '' :
        user_input = 'AMZN'

    '''Quandl API request'''
    quandl = os.environ['Quandl_SECRET']

    yesterday = date.today() - timedelta(days=1)
    last_month = yesterday - monthdelta(1)
    yesterday = yesterday.strftime('%Y-%m-%d')
    last_month = last_month.strftime('%Y-%m-%d')

    ticker = 'https://www.quandl.com/api/v3/datasets/WIKI/AAPL?trim_start=2018-02-15&trim_end=2018-03-23&api_key=PlaceKeyHere'
    ticker = ticker.replace('AAPL', user_input)
    ticker = ticker.replace('PlaceKeyHere', quandl)
    ticker = ticker.replace('2018-02-15', last_month)
    ticker = ticker.replace('2018-03-23', yesterday)

    r = requests.get(ticker)

    #create dictionary of API call:
    d = r.json()

    #these are the columns names:
    # ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Ex-Dividend', 'Split Ratio', 'Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']
    try:
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

        fname = 'user_input_stock_ticker.html'
        # html = file_html(p1, CDN, fname)

        script, div = components(p1)
        html = script + div

    except :
        html = 'No such company.'
    return html

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
  app.run()
