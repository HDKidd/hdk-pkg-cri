# -*- coding: utf-8 -*-
"""
@author: He Dekun
"""

import numpy as np
import pandas as pd
from statsmodels.distributions.empirical_distribution import ECDF

#HA_Open = HA_Open_lb
#HA_Close = HA_Close_1b

def func_PS_Level(HA_Open, HA_Close, PS_pct_level=[0.35, 0.5, 0.95, 0.97], combine=False):
    """
    0. This function is for calculating the HA bars' bar size level, or called Price Status(PS).
    1. This function has 4 arguments and return 2 arrays as output.
    2. Input arguments including:
        (1) HA_Open: DataFrame.
        (2) HA_Close: DataFrame.
        (3) PS_pct_level: list, optional, default value is [0.35, 0.5, 0.95, 0.97]
        （4) combine: boolean, optional, default value is False, calculating the up bar and down bar separately, 
                     while combine=True calculates the up bar and down bar combined.
    3. Output are 2 arrays with 4 level values in each, including:
        (1) HA_PS_positive_level
        (2) HA_PS_negative_level
    """
    
    # Initialize:
    HA_num  = len(HA_Close)
    HA_level_num = len(PS_pct_level)
    HA_bar_size = np.zeros((HA_num,1))
    
    HA_bar_positive_size = np.zeros((HA_num,1))
    HA_bar_negative_size = np.zeros((HA_num,1))
    HA_PS_positive_level = np.zeros((HA_level_num,1))
    HA_PS_negative_level = np.zeros((HA_level_num,1))
    
    HA_positive_count = 0 
    HA_negative_count = 0 
    
    # HA_size & HA_ECDF
    if combine == True:
        HA_bar_size = abs(HA_Close - HA_Open)
        HA_bar_positive_size = HA_bar_size
        HA_bar_negative_size = -HA_bar_size

    if combine == False:  
        # HA_size & HA_ECDF
        for i in range(0, HA_num):
            HA_bar_size[i, 0] = HA_Close[i] - HA_Open[i]
            
            if HA_bar_size[i, 0] > 0:
                HA_positive_count += 1
                HA_bar_positive_size[HA_positive_count-1, 0] = HA_bar_size[i, 0]
            if HA_bar_size[i, 0] < 0:
                HA_negative_count += 1
                HA_bar_negative_size[HA_negative_count-1, 0] = HA_bar_size[i, 0]
        
        if HA_positive_count == 0:
            HA_bar_positive_size = HA_bar_positive_size[0:HA_negative_count, 0]
        else:
            HA_bar_positive_size = HA_bar_positive_size[0:HA_positive_count, 0]
        if HA_negative_count == 0:
            HA_bar_negative_size = HA_bar_negative_size[0:HA_positive_count, 0]
        else:
            HA_bar_negative_size = HA_bar_negative_size[0:HA_negative_count, 0]
        
    HA_positive_size = ECDF(HA_bar_positive_size).x
    HA_positive_ecdf = ECDF(HA_bar_positive_size).y
    HA_negative_size = ECDF(-HA_bar_negative_size).x
    HA_negative_ecdf = ECDF(-HA_bar_negative_size).y
    
    # Match ecdf with HA_bar_pct_level
    for n in range(0, HA_level_num):
        HA_PS_positive_level_idx = np.where(HA_positive_ecdf <= PS_pct_level[n])[0][-1]
        HA_PS_positive_level[n]  = HA_positive_size[HA_PS_positive_level_idx] 
        HA_PS_negative_level_idx = np.where(HA_negative_ecdf <= PS_pct_level[n])[0][-1]
        HA_PS_negative_level[n]  = -HA_negative_size[HA_PS_negative_level_idx] 

    return HA_PS_positive_level, HA_PS_negative_level


#HA_Open = data_HA.HA_Open
#HA_Close = data_HA.HA_Close
#HA_PS_Lookback=PS_window
def func_BarPS(HA_Open, HA_Close, HA_PS_Lookback, PS_pct_level=[0.35, 0.5, 0.95, 0.97], combine=False):
    """
    0. This function is for calculating price trend number of HA bar, by looking back HA_PS_Lookback HA bars,
       according to the previous bars' distribution, find the range (i.e. -4,-3,-2,-1,0,1,2,3,4) of the current bar.
    1. This function has 5 arguments (one optional) and returns 1  DataFrame as output.
    2. Input arguements including:
        (1) HA_Open: Dataframe
        (2) HA_Close: DataFrame
        (3) HA_PS_Lookback: int, number of bars to lookback.
        (4) PS_pct_level: list, optional, default value is [0.35, 0.5, 0.95, 0.97]
        (5) combine: boolean, optional, default value is False, calculating the up bar and down bar separately, 
                     while combine=True calculates the up bar and down bar combined.
    3. Output is 1 DataFrame
        (1) HA_PS: Showed as -4,3,-2,-1,0,1,2,3,4, indicating the size of HA bars.   
    """
    
    # Initialize:
    HA_num  = len(HA_Open)
    HA_PS = np.zeros_like(HA_Open)
    
    HA_Open = HA_Open.values
    HA_Close = HA_Close.values
    
    # Main:
    for i in range(HA_PS_Lookback, HA_num):
        
        HA_Open_lb  = HA_Open [i-HA_PS_Lookback:i]
        HA_Close_1b = HA_Close[i-HA_PS_Lookback:i]
        HA_PS_positive_level, HA_PS_negative_level = func_PS_Level(HA_Open_lb, HA_Close_1b, PS_pct_level, combine)
        HA_range = HA_Close[i] - HA_Open[i]

        if HA_range > 0:
            HA_PS_temp = np.where(HA_range <= HA_PS_positive_level)[0] + 1
            if len(HA_PS_temp) != 0:
                HA_PS[i] = HA_PS_temp[0] - 1
            else:
                HA_PS[i] = len(HA_PS_positive_level) # -1
    
        if HA_range < 0:
            HA_PS_temp = np.where(HA_range >= HA_PS_negative_level)[0] + 1
            if len(HA_PS_temp) != 0:
                HA_PS[i] = -HA_PS_temp[0] + 1
            else:
                HA_PS[i] = -len(HA_PS_negative_level) # +1

    HA_PS_df = pd.DataFrame(HA_PS, columns=['PS'])
    
    return HA_PS_df