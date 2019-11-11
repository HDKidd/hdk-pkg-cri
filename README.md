# hdk_pkg_cri

This is a demo package for CRI test. 
This package is for processing kline data and running strategy backtest. 


## 1 Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install hdk_pkg_critest.

```bash
pip install hdk_pkg_cri
```


## 2 Quick Start

The package can be run on shell or CMD, but better to use an IDE (Try [Spyder](https://www.spyder-ide.org/) that check the outputs easily). 

This chapter gives a simple demo of doing a momentum strategy backtest using the package. All the codes can also be found in `demo.py`.

Please refer to next chapter for detailed documentation on the package.

### STEP 1: Import the Package and Initialization

First, let's import the package, and initialize four core classes. 
Once you initialize an instance of a class, you can easily call methods (functions) from it by doing this: `return = instance.function(Args..)`

```python
from hdk_pkg import critest

sampledata = critest.SampleData()    # a class for fetching the sample data set
process = critest.Process()    # a class for processing data
backtest = critest.BackTest()    # a class for running backtesting
plotting = critest.Plotting()    # a class for Plotting the backtest results
```

### STEP 2: Get a Sample Data Set for Test

Then, Let's use the `get_sampledata()` from the `sampledata` to get a sample data set. Use `data.head()` to check the data.

```python
data = sampledata.get_SampleData()    # a time-series data set of a future's kline 

data.head()    # check what the data set looks like
```

### STEP 3: Process the Data to Generate Factors

There are some kline process funcions in the class `process`. You can call and apply them on the data. For a momentum strategy, we need to process the kline as below:

```python
#1 transfer the 1min kline to 60mins kline:
data_60 = process.chg_Granularity(data_1min=data, granularity=60)
data_60.head() 

#2 generate HA kline:
data_HA = process.get_BarHA(Open=data_60.open, High=data_60.high, Low=data_60.low, Close=data_60.close)
data_HA.head() 

#3 generate PS factor:
data_PS = process.get_BarPS(HA_Open=data_HA.HA_Open, HA_Close=data_HA.HA_Close, HA_PS_Lookback=20, PS_pct_level=[0.35, 0.5, 0.95, 0.97], combine=False)
data_PS.head() 

#4 generate CT factor:
data_CT = process.get_BarCT(HA_Open=data_HA.HA_Open, HA_Close=data_HA.HA_Close, HA_PS=data_PS, bar_pass_cut=2, ps_pass_cut=2)
data_CT.head() 
```

### STEP 4: Generate Buy Sell Indicators and Do Backtest

Now we should use it to generate buy sell indicators. This should follow some specific rules based on different strategies. 
(I have only built in one strategy rule called "momentum". In fact, other strategies can be add inside the package easily.) 

Call `backtest_Momentum()` from class `backtest`, then you will get a return as matrix (two-dimensional array). 
The buy sell indicator is in 4th column. We can use it to do backtest by calling `get_PnL()`.

```python
backtest_Momentum = backtest.backtest_Momentum(data_PS=data_PS, data_CT=data_CT.bar_idx_live)
print (backtest_Momentum)    # see the return matrix

result = backtest.get_PnL(close=data_60.close, indicator=backtest_Momentum[:,2], cost=0.15/100, sharpe_frequency=365*2, beta=1)
print (result)    # see the backtest result
```

### STEP 5: Plot the Backtest Result

Finally, you can plot a custom image based on the backtest result.

```python
plot1 = plotting.plot_type1(Open=data_60.open, High=data_60.high, Low=data_60.low, Close=data_60.close, indicator=backtest_Momentum[:,2], result=result)
```


## 3 Documentation for Functions

### SampleData: get_SampleData()

```python
re = sampledata.get_sampledata()
"""
This function is for fetching the sample data set.

Args: None

Returns: Returns a Dataframe with a time index and 5 coumns, inclding:
         (1) open: Float. 
         (2) high: Float. 
         (3) low: Float. 
         (4) close: Float. 
         (5) volume: Float. 
"""
```

### Process: chg_Granularity()

```python
re = process.chg_Granularity(data_1min, granularity)
"""
This function is for changing the granularity of kline from 1min to N mins.

Args: 
     (1) data_1min: Dataframe. 1min kline data with column names as 'open', 'high', 'low', 'close' and 'volume'; with index by time.
     (2) granularity: Int. The desired time granularity, minute based, for example, if you want hour kline, set granularity=60.

Returns: Returns a Dataframe with a adjusted-time index and 5 coumns, inclding:
        (1) open: Float. 
        (2) high: Float. 
        (3) low: Float. 
        (4) close: Float. 
        (5) volume: Float. 
"""
```

### Process: get_BarHA()

```python
re = process.get_BarHA(Open, High, Low, Close)
"""
This function is for transferring normal Bar to Heikin Ashi Bar.

Args: 
     (1) Open: Dataframe with values in Float type.
     (2) High: Dataframe with values in Float type.
     (3) Low: Dataframe with values in Float type.
     (4) Close: Dataframe with values in Float type.

Returns: Returns a Dataframe with 4 coumns, inclding:
        (1) HA_Open: Float. 
        (2) HA_High: Float.
        (3) HA_Low: Float. 
        (4) HA_Close: Float. 
"""
```

### Process: get_BarPS()

```python
re = process.get_BarPS(HA_Open, HA_Close, HA_PS_Lookback, PS_pct_level=[0.35, 0.5, 0.95, 0.97], combine=False)
"""
This function is for calculating price trend number of HA bar, by looking back HA_PS_Lookback HA bars,
according to the previous bars' distribution, find the range (i.e. -4,-3,-2,-1,0,1,2,3,4) of the current bar.

Args: 
     (1) HA_Open: Dataframe with values in Float type.
     (2) HA_Close: DataFrame with values in Float type.
     (3) HA_PS_Lookback: int, number of bars to lookback.
     (4) PS_pct_level: list, optional, default value is [0.35, 0.5, 0.95, 0.97]
     (5) combine: boolean, optional, default value is False, calculating the up bar and down bar separately, 
                  while combine=True calculates the up bar and down bar combined.

Returns: Returns a Dataframe with 1 coumns, inclding:
        (1) HA_PS: Int. 

"""
```

### Process: get_BarCT()

```python
re = process.get_BarCT(HA_Open, HA_Close, HA_PS, bar_pass_cut=2, ps_pass_cut=2)
"""
This function is for counting indices of continuously up or down bar (skipping some small-ps bar).

Args: 
     (1) HA_Open, HA_Close, HA_PS, all are DataFrame.
     (2) bar_pass_cut: int, optional, default is 2, number of small opposite bars we can skip.
     (3) ps_pass_cut: int, optional, default is 2, ps cut level of oppsite bar we can skip.

Returns: Returns a Dataframe with 3 coumns, inclding:
        (1) bar_len: HA bar trend cycle length, up trend being positive number, while down trend being negative.
        (2) bar_idx: count bar index, always starts from 1 or -1, would use future data to update current count index. (Use this carefully)
        (3) bar_idx_live: cout bar index, may start from numbers larger than 1, would not use furture data.

"""
```
### BackTest: backtest_Momentum()

```python
re = backtest.backtest_Momentum(data_PS, data_CT)
"""
This function is for generating the buy sell indicator under momentum strategy rules.

Args: 
     (1) data_PS: 1 column Dataframe with values in Int type.
     (2) data_CT: 1 column Dataframe with values in Int type.

Returns: Returns a array with 4 columns, inclding:
        (1) data_PS: Int. Input values
        (2) data_CT: Int. Input values
        (3) indicator: Int. The buy sell indicator
        (4) buysell type: Int. Indicate the rule number that the buy sell indicator is followed.

"""
```
### BackTest: get_PnL()

```python
re = backtest.get_PnL(close, indicator, cost, sharpe_frequency, beta=1)
"""
This function is for calculating backtest outputs.

Args: 
     (1) close: array, close price in time series.
     (2) indicator: array, buy sell indicator in time series.
     (3) cost: float, cost percentage.
     (4) sharpe_frequency: int, number of observations in one year

Returns: Returns a list with 3 elements, inclding:
        (1) Return: List. Return list.
        (2) Trade_number: Int. Times have trade.
        (3) Annual_Sharpe: Float. Annual sharpe ratio.

"""
```
### Plotting: plot_type1()

```python
re = plotting.plot_type1(Open, High, Low, Close, indicator, result)
"""
This function is for plotting the backtest result in custom type 1.

Args: 
     (1) Open: Dataframe with values in Float type.
     (2) High: Dataframe with values in Float type.
     (3) Low: Dataframe with values in Float type.
     (4) Close: Dataframe with values in Float type.
     (5) indicator: Array. The buy sell indicator.
     (6) result: List. The backtest result.

Returns: Returns a figure.
"""
```


## 4 Author
He Dekun

## 5 License
[MIT](https://choosealicense.com/licenses/mit/)

