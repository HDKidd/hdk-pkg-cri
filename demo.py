# -*- coding: utf-8 -*-
"""
@author: He Dekun

Instructions:
    
1) This is a demo to do backtest on a momentum strategy. Follow the steps to get a backtest result.
2) This demo only show some commonly used functions, pls refer to readme.md for more functions.
3) You can press "Ctrl+Enter" to run the demo cell by cell, or press "F5" to run the whole demo.
"""

#%% import and initialization
from hdk_pkg import critest

# initialize instances from four classes:
sampledata = critest.SampleData()    # class to get sample price data
process = critest.Process()    # class to process price data
backtest = critest.BackTest()    # class to run backtest based on specific strategy
plotting = critest.Plotting()    # plot the backtest result

#%% get sample data (you could also load your personal data):
data = sampledata.get_SampleData()
print ('get data_1min finished!')
data.head()

#%% transfer the 1min kline to 60mins kline:
data_60 = process.chg_Granularity(data_1min=data, granularity=60)
print ('get data_60min finished!')
data_60.head()

#%% generate HA kline:
data_HA = process.get_BarHA(Open=data_60.open, High=data_60.high, Low=data_60.low, Close=data_60.close)
print ('get_BarHA finished!')
data_HA.head()

#%% generate PS factor:
data_PS = process.get_BarPS(HA_Open=data_HA.HA_Open, HA_Close=data_HA.HA_Close, HA_PS_Lookback=20, PS_pct_level=[0.35, 0.5, 0.95, 0.97], combine=False)
print ('data_PS finished!')
data_PS.head()

#%% generate CT factor:
data_CT = process.get_BarCT(HA_Open=data_HA.HA_Open, HA_Close=data_HA.HA_Close, HA_PS=data_PS, bar_pass_cut=2, ps_pass_cut=2)
print ('data_CT finished!')
data_CT.head()

#%% generate buy sell indicator based on a simple momentum strategy:
backtest_Momentum = backtest.backtest_Momentum(data_PS=data_PS, data_CT=data_CT.bar_idx_live)
print ('backtest on momentum strategy finished!')
print(backtest_Momentum)

#%% do backtest and generate the PnL results:
result = backtest.get_PnL(close=data_60.close, indicator=backtest_Momentum[:,2], cost=0.15/100, sharpe_frequency=365*2, beta=1)
print ('get backtest PnL finished!')
print(result)

#%% plot the results:
plot1 = plotting.plot_type1(Open=data_60.open, High=data_60.high, Low=data_60.low, Close=data_60.close, indicator=backtest_Momentum[:,2], result=result)

