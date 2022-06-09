from time import strftime
import yfinance as yf
import datetime
import dash
from dash import dcc, html
from dateutil import relativedelta
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = dash.Dash()
server = app.server

def serve_layout():
    hour = int(datetime.datetime.now().strftime("%I")) - 4
    return html.Div(children=[
        html.H2("Live Stock Chart as of " + datetime.datetime.now().strftime("%m/%d/%Y ") + str(hour) + datetime.datetime.now().strftime(":%M")),

        html.Div(children='Period: ', style={'display': 'block'}),
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

        html.Div(children='Ticker: ',style={'display': 'inline-block', 'padding-left': '11vw', 'padding-right': '1vw'}),
        dcc.Input(id='input', value='', type='text',persistence=True,style={'display': 'inline-block','width': '4vw'}),
        html.Div(children='Ticker: ',style={'display': 'inline-block', 'padding-left': '21vw', 'padding-right': '1vw'}),
        dcc.Input(id='input2', value='', type='text',persistence=True,style={'display': 'inline-block','width': '4vw'}),
        html.Div(children='Ticker: ',style={'display': 'inline-block', 'padding-left': '21.75vw', 'padding-right': '1vw'}),
        dcc.Input(id='input3', value='', type='text',persistence=True,style={'display': 'inline-block','width': '4vw'}),
        
        dcc.Graph(id='graph1',style={'display': 'inline-block', 'width': '30vw', 'height' : '35vh'}),
        dcc.Graph(id='graph2',style={'display': 'inline-block', 'width': '30vw', 'height' : '35vh'}),
        dcc.Graph(id='graph3',style={'display': 'inline-block', 'width': '30vw', 'height' : '35vh'}),

        html.Div(children='Ticker: ',style={'display': 'inline-block', 'padding-left': '11vw', 'padding-right': '1vw'}),
        dcc.Input(id='input4', value='', type='text',persistence=True,style={'display': 'inline-block','width': '4vw'}),
        html.Div(children='Ticker: ',style={'display': 'inline-block', 'padding-left': '21vw', 'padding-right': '1vw'}),
        dcc.Input(id='input5', value='', type='text',persistence=True,style={'display': 'inline-block','width': '4vw'}),
        html.Div(children='Ticker: ',style={'display': 'inline-block', 'padding-left': '21.75vw', 'padding-right': '1vw'}),
        dcc.Input(id='input6', value='', type='text',persistence=True,style={'display': 'inline-block','width': '4vw'}),

        dcc.Graph(id='graph4',style={'display': 'inline-block', 'width': '30vw', 'height' : '35vh'}),
        dcc.Graph(id='graph5',style={'display': 'inline-block', 'width': '30vw', 'height' : '35vh'}),
        dcc.Graph(id='graph6',style={'display': 'inline-block', 'width': '30vw', 'height' : '35vh'}),
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

@app.callback(
    Output('graph4', 'figure'),
    Input('input4', 'value'),
    Input('interval_dropdown', 'value')
)
def update_graph(input_ticker: str, interval):
    return update_grapher(input_ticker, interval)

@app.callback(
    Output('graph5', 'figure'),
    Input('input5', 'value'),
    Input('interval_dropdown', 'value')
)
def update_graph(input_ticker: str, interval):
    return update_grapher(input_ticker, interval)

@app.callback(
    Output('graph6', 'figure'),
    Input('input6', 'value'),
    Input('interval_dropdown', 'value')
)
def update_graph(input_ticker: str, interval):
    return update_grapher(input_ticker, interval)


if __name__ == "__main__":
    app.run_server(debug=True)