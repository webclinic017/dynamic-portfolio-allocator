from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from strategies.BasePortfolio import BasePortfolio

from components.navbar import navbar

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

cp = BasePortfolio("Classic 60/40 Portfolio", ["SPY", "IEF"], [0.6, 0.4])
pp = BasePortfolio("Permanent Portfolio", ["VTI", "BIL", "TLT", "GLD"], [0.25, 0.25, 0.25, 0.25])
allSeason = BasePortfolio("All Season Portfolio", ["SPY", "TLT", "IEF", "DBC", "GLD"], [0.3, 0.4, 0.15, 0.075, 0.075])


def update_table():
    data = {
        "Allocation": [str(cp), str(pp), str(allSeason)],
        "CAGR": [cp.cagr(), pp.cagr(), allSeason.cagr()],
        "MDD": [cp.mdd(), pp.mdd(), allSeason.mdd()],
    }
    df = pd.DataFrame(data)

    return df.to_dict("records")


def update_graph():
    df = pd.DataFrame()

    df[str(cp)] = cp.port_cum_returns()
    df[str(pp)] = pp.port_cum_returns()
    df[str(allSeason)] = allSeason.port_cum_returns()
    df.reset_index(inplace=True)
    print(df)
    return px.line(df, x="Date", y=[col for col in df.columns if col != "Date"], title="Historical Portfolio Returns")
    # return px.line(df, x="Date", y=[col for col in df.columns if col != "Date"])


app.layout = html.Div(
    [
        navbar,
        dcc.Graph(figure=update_graph(), id="total-perf-graph"),
        html.Div(
            [
                dash_table.DataTable(
                    update_table(),
                    id="total-perf-table",
                )
            ]
        ),
    ]
)


if __name__ == "__main__":
    app.run(debug=True)
