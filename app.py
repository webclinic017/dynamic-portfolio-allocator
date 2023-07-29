from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

from components.navbar import navbar

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        navbar,
        dcc.Graph(id="total-perf-graph"),
        html.Div([dash_table.DataTable(id="total-perf-table")]),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
