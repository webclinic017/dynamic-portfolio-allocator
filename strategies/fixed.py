import datetime as dt
import pandas as pd
import numpy as np
import yfinance as yf


class FixedPortfolio:
    def __init__(self, assets, weights) -> None:
        self.assets = assets
        self.weights = weights

    def monthly_returns(self):
        # monthly returns
        prices = yf.download(self.assets, start="2020-01-01", end=dt.datetime.today(), interval="1mo")
        prices = prices.loc[:, "Adj Close"]
        prices.columns = self.assets
        monthly_returns = prices.pct_change().dropna()
        return monthly_returns

    def port_cum_returns(self):
        # portfolio cumulative returns
        monthly_returns = self.monthly_returns()
        monthly_returns = monthly_returns.shift(-1)
        monthly_returns["port"] = monthly_returns.dot(self.weights)
        cum_returns = np.exp(np.log1p(monthly_returns["port"]).cumsum())[:-1]
        return cum_returns

    def cagr(self):
        port_cum_returns = self.port_cum_returns()
        first_value = port_cum_returns[0]
        last_value = port_cum_returns[-1]
        years = len(port_cum_returns.index) / 12
        cagr = (last_value / first_value) ** (1 / years) - 1
        return cagr

    def mdd(self):
        port_cum_returns = self.port_cum_returns()
        previous_peaks = port_cum_returns.cummax()
        drawdown = (port_cum_returns - previous_peaks) / previous_peaks
        port_mdd = drawdown.min()
        return port_mdd


if __name__ == "__main__":
    cp = FixedPortfolio(["SPY", "IEF"], [0.6, 0.4])
    print(cp.cagr())
    print(cp.mdd())
    print(cp.monthly_returns())
