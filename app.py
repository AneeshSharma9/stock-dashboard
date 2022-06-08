from multiprocessing.connection import wait
from turtle import width
import yfinance as yf
import datetime
import dash
from dash import dcc, html
from dateutil import relativedelta
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import time

app = dash.Dash()
server = app.server

def serve_layout():
    return html.Div(children=[
        html.H1(children="Live Stock Chart"),
        html.H2('Prices as of ' + datetime.datetime.now().strftime("%m/%d/%Y %I:%M")),

        html.Div(children='Ticker: ',style={'display': 'inline-block', 'padding-left': '12%'}),
        dcc.Input(id='input', value='', type='text',persistence=True,style={'display': 'inline-block','width': '5%'}),
        html.Div(children='Ticker: ',style={'display': 'inline-block', 'padding-left': '24%'}),
        dcc.Input(id='input2', value='', type='text',persistence=True,style={'display': 'inline-block','width': '5%'}),
        html.Div(children='Ticker: ',style={'display': 'inline-block', 'padding-left': '24%'}),
        dcc.Input(id='input3', value='', type='text',persistence=True,style={'display': 'inline-block','width': '5%'}),

        html.Div(children='Interval: '),
        dcc.Dropdown(id = 'interval_dropdown',
            options = [
                {'label': '1D', 'value' : '1D'},
                {'label': '1M', 'value' : '1M'},
                {'label': '1Y', 'value' : '1Y'},
                {'label': '5Y', 'value' : '5Y'}
            ],
            value='1M',
            persistence=True,
            style={'width': '25%'}
        ),
        dcc.Graph(id='graph1',style={'display': 'inline-block', 'width': '32%'}),
        dcc.Graph(id='graph2',style={'display': 'inline-block', 'width': '32%'}),
        dcc.Graph(id='graph3',style={'display': 'inline-block', 'width': '32%'}),
    ])

app.layout = serve_layout

def update_grapher(input_ticker: str, interval):

    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime.today()
    if interval == '1D':
        start = end - datetime.timedelta(1)
    elif interval == '1M':
        start = end - relativedelta.relativedelta(months = 1)
    elif interval == '1Y':
        start = end - relativedelta.relativedelta(years = 1)
    elif interval == '5Y':
        start = end - relativedelta.relativedelta(years = 5)

    if interval == '1D':
        #df = yf.download(tickers=input_ticker,period='1D',interval='2m')
        df = yf.Ticker(input_ticker).history(period = '1D', interval='2m')
    else:
        df = yf.Ticker(input_ticker).history(start=start, end=end)
    
    
    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

    if interval == '1D':
        figure={
            'data': [{'x': df.index, 'y': df['Close'], 'type': 'line',
                      'name': 'stock price graph', 'color': 'red'}],
            'layout': {
                'title': f'{input_ticker}'.upper()
                }
            }
    else:
        figure=go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
        figure.update_layout(title_text=input_ticker.upper(), title_x=0.5)

   
    return figure

@app.callback(
    Output('graph1', 'figure'),
    Input('input', 'value'),
    Input('interval_dropdown', 'value')
)
def update_graph(input_ticker: str, interval):
    return update_grapher(input_ticker, interval)


@app.callback(
    Output('graph2', 'figure'),
    Input('input2', 'value'),
    Input('interval_dropdown', 'value')
)
def update_graph(input_ticker: str, interval):
    return update_grapher(input_ticker, interval)

@app.callback(
    Output('graph3', 'figure'),
    Input('input3', 'value'),
    Input('interval_dropdown', 'value')
)
def update_graph(input_ticker: str, interval):
    return update_grapher(input_ticker, interval)


if __name__ == "__main__":
    app.run_server(debug=True)