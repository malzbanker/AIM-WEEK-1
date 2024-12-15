import yfinance as yf
import talib as ta
import numpy as np
import pandas as pd
import plotly.express as px
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns


class FinancialAnalyzer:
    def __init__(self,ticker,start_date,end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date

    def retriev_stock_data(self):
        return yf.download(self.ticker, start = self.start_date, end = self.end_date)

    def calculate_moving_average(self,data,window_size):
        return ta.SMA(data,timeperiod=window_size)
    
    def calculate_technical_indicators(self,data):
        # calculate various technical indicators
        data['SMA']=self.calculate_moving_average(data['Close'],20)
        data['RSI']=ta.RSI(data['Close'],timeperiod=14)
        data['EMA']=ta.EMA(data['Close'],timeperiod=20)
        macd,macd_signal,_ = ta.MACD(data['Close'])
        data['MACD']=macd
        data['MACD_Signal']=macd_signal
        return data
    
    def plot_stock_data(self,data):
        fig = px.line(daat,x=data.index,y=['Close','SMA'],title='Stock price with')
        fig.show()

    def plot_rsi(self,data):
        fig=px.line(data, x=data.index, y='RSI', title='Relative Strength index (RSI)')
        fig.show()

    def plot_ema(self,data):
        fig=px.line(data, x=data.index ,y=['Close','EMA'],title='Stock price with Exponential')
        fig.show()

    def plot_macd(self,data):
        fig=px.line(data, x=data.index ,y=['MACD','MACD_Signal'],title='Moving Average Exponential')
        fig.show()

    def calculate_portfolio_weights(self,tickers,start_date,end_date):
        data=yf.download(tickers,start=start_date,end=end_date)['Close']
        mu=expected_returns.mean_historical_returns(data)
        cov=risk_models.sample_cov(data)
        ef=EfficientFrontier(mu,cov)
        weights=ef.max_sharpe()
        weights=dict(zip(tickers,weights.values()))
        return weights
    
    def calculate_portfolio_performance(self,tickers,start_date,end_date):
        data=yf.download(tickers,start=start_date,end=end_date)['Close']
        mu=expected_returns.mean_historical_returns(data)
        cov=risk_models.sample_cov(data)
        ef=EfficientFrontier(mu,cov)
        weights=ef.max_sharpe()
        portfolio_returns,portfolio_volatility,sharpe_ratio=ef.portfolio_performance()
        return portfolio_returns,portfolio_volatility,sharpe_ratio