# -*- coding: utf-8 -*-
"""
@author: He Dekun
"""

from . sampledata import data
from . process import func_BarHA, func_BarPS, func_BarCount, func_ChangeGranularity
from . backtest import func_Status, func_Momentum
from . plotting import func_plot_type1


class SampleData(object):
    
    def __init__(self):
        self.name = 'SampleData'
        
    def get_SampleData(self):
        return data.data()


class Process(object):
    
    def __init__(self):
        self.name = 'Process'
        
    def chg_Granularity(self, data_1min, granularity):
        return func_ChangeGranularity.func_ChangeGranularity(data_1min, granularity)
    
    def get_BarHA(self, Open, High, Low, Close):
        return func_BarHA.func_BarHA(Open, High, Low, Close)
    
    def get_BarPS(self, HA_Open, HA_Close, HA_PS_Lookback, PS_pct_level=[0.35, 0.5, 0.95, 0.97], combine=False):
        return func_BarPS.func_BarPS(HA_Open, HA_Close, HA_PS_Lookback, PS_pct_level, combine)
    
    def get_BarCT(self, HA_Open, HA_Close, HA_PS, bar_pass_cut=2, ps_pass_cut=2):
        return func_BarCount.func_BarCount(HA_Open, HA_Close, HA_PS, bar_pass_cut, ps_pass_cut)


class BackTest(object):
    
    def __init__(self):
        self.name = 'BackTest'
        
    def backtest_Momentum(self, data_PS, data_CT):
        return func_Momentum.func_Momentum(data_PS, data_CT)

    def get_PnL(self, close, indicator, cost, sharpe_frequency, beta=1):
        return func_Status.func_Status(close, indicator, cost, sharpe_frequency, beta)
    
    
class Plotting(object):
    
    def __init__(self):
        self.name = 'Plotting'
        
    def plot_type1(self, Open, High, Low, Close, indicator, result):
        return func_plot_type1.func_plot_type1(Open, High, Low, Close, indicator, result)
    