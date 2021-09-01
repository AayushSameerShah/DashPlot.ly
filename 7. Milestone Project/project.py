import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

from pandas.core.indexes import multi
import plotly.graph_objs as go

import pandas as pd
import pandas_datareader as pdr
from datetime import date

nasdaq = pd.read_pickle("./nasdaq")

'''Main Page'''
app = dash.Dash()

'''Individual Widgets'''
# 1.
drop_down = dcc.Dropdown(
                options=[
                    {"label":face_value, "value":value}
                    for value, face_value in nasdaq.values
                ],
                multi=True,
                id="stocks_picker"
            )   

# 2.
date_picker = dcc.DatePickerRange(
                id='date_picker',
                min_date_allowed = date(2000, 1, 1),
                start_date = date(2016, 1, 1),
                start_date_placeholder_text = 'From Date', 
                end_date_placeholder_text = 'To Date', 
            )

app.layout = html.Div(children=[
                html.Div([
                    html.Label("Choose Stock(s)"),
                    drop_down
                    ], style={"display":"inline-block", 
                          "width":"40%"}
                ),
                html.Div([
                    html.Label("Choose Date Range (Choose nothing for all data)"),
                    date_picker
                    ], style={"display":"inline-block", 
                          "width":"40%"}
                ),
                html.Div([
                    html.Button(children="Get Data", id="submit")
                    ], style={"display":"inline-block", 
                          "width":"10%"}
                ),
                html.Div([
                    dcc.Graph(id="graph")
                    ]
                ),
    
])

@app.callback(Output("graph", "figure"),
             [Input("submit", "n_clicks")],
             [State("stocks_picker", "value"),
              State("date_picker", "start_date"),
              State("date_picker", "end_date")])
def update_values(_, stocks, start_date, end_date):
    print(stocks, start_date, end_date, end="\n-----------\n")
    if stocks:
        all_stocks = []
        for stock in stocks:
            data = pdr.get_data_yahoo(stock, start_date, end_date)["Close"].rename(stock)
            all_stocks.append(data)
        all_stocks = pd.DataFrame(all_stocks).T
        
        traces = [go.Scatter(x=all_stocks.index,
                             y=all_stocks[stock],
                             mode='lines',
                             name=stock)
                 for stock in all_stocks.columns]
        layout = go.Layout(title=f"The stock prices of {len(all_stocks.columns)} stocks")
        figure = go.Figure(data=traces, layout=layout)
        return figure
    return None

app.run_server()