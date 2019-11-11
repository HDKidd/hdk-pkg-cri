# -*- coding: utf-8 -*-
"""
@author: He Dekun
"""

import numpy as np

def func_Status(close, indicator, cost, sharpe_frequency, beta=1):
    """
    0. This function is for calculating backtest outputs.
    1. This function has 4 arguements and returns 1 list with 3 elements as output.
    2. Input arguments including:
        (1) close: array, close price in time series.
        (2) indicator: array, buy sell indicator in time series.
        (3) cost: float, cost percentage.
        (4) sharpe_frequency: int, number of observations in one year.
    3. Output 1 list with 3 elements:
        (1) Return: list.
        (2) Trade_number.
        (3) Annual_Sharpe.
    """
    
    # Initialize:
    Return = np.zeros(len(indicator))
    start = 0
    Trade_number = 0
    
    # Main:
    for i in range(2, len(indicator)):
        
        if indicator[i-1] == 0:
            Return[i] = Return[i-1]
        
        if indicator[i-1] == 1:
            if indicator[i-2] != 1:
                start = i-1
                Trade_number += 1
                Return[i-1] = Return[i-1] - cost
            Return_delta = (close[i] - close[i-1]) / close[start] * beta
            Return[i] = Return[i-1] + Return_delta
        
        if indicator[i-1] == -1:
            if indicator[i-2] != -1:
                start = i-1
                Trade_number += 1
                Return[i-1] = Return[i-1] - cost
            Return_delta = (close[i-1] - close[i]) / close[start] * beta
            Return[i] = Return[i-1] + Return_delta
    
    diff = Return[1:] - Return[:-1]
    Annual_Sharpe = np.mean(diff) / np.std(diff) * np.sqrt(sharpe_frequency)
    
    return Return, Trade_number, Annual_Sharpe