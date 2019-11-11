# -*- coding: utf-8 -*-
"""
@author: He Dekun
"""

import pandas as pd

def func_1min2day(data_min, cut_time_gap=5/24):
    """
    0. This function is for transferring a 1min bar to 1day bar, must has non-trading time over 5 hours in one day.
    1. This function has 1 argument and returns 1 Dataframe with 5 columns as output.
    2. Input argument:
        data_min: must be as Dataframe format, with 5 columns including 'time', 'high', 'low', 'close', 'open'.
    3. Output is a Dataframe with 5 columns including 'time_d', 'high_d', 'low_d', 'close_d', 'open_d'.
    
    NOTE:
        No need to change the input Dataframe's column names.
    """
    
    # Initialize:
    cut_time_gap = cut_time_gap   # for gapping time more than 5 hours
    df_input = pd.DataFrame()
    df_output = pd.DataFrame()
    
    for i in ['time', 'high', 'low', 'close', 'open']:
        for c in data_min.columns:
            if i in c:
                df_input[i] = data_min[c]
    
    time_d, high_d, low_d, close_d, open_d = [], [], [], [], []
    last_close = -1
    num_1min = len(data_min)
    
    # Main：
    for i in range(0, num_1min-1):
        if (df_input.time[i+1] - df_input.time[i]) > cut_time_gap:
            time_d.append(df_input.time[i])
            open_d.append(df_input.open[last_close+1])
            close_d.append(df_input.close[i])
            high_d.append(max(df_input.high[last_close+1:i]))
            low_d.append(min(df_input.low[last_close+1:i]))
            last_close = i
            
        if (i==num_1min-2) and ((df_input.time[i+1]-df_input.time[i]) <= cut_time_gap):
            time_d.append(df_input.time[i+1])
            open_d.append(df_input.open[last_close+1])
            close_d.append(df_input.close[i+1])
            high_d.append(max(df_input.high[last_close+1:i+1]))
            low_d.append(min(df_input.low[last_close+1:i+1]))
    
    data_dict = {'time_d':time_d, 'high_d':high_d, 'low_d':low_d, 'close_d':close_d, 'open_d':open_d}
    df_output = pd.DataFrame(data_dict)
    df_output = df_output[['time_d', 'high_d', 'low_d', 'close_d', 'open_d']]
    
    return df_output