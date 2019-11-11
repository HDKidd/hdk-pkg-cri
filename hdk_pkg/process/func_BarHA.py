# -*- coding: utf-8 -*-
"""
@author: He Dekun
"""

import pandas as pd
from copy import deepcopy

def func_BarHA(Open, High, Low, Close):
    """
    0. This function is for transferring normal Bar to Heikin Ashi Bar.
    1. This function has 4 arguements and returns 1 Dataframe with 4 columns as output.
    2. Input arguments including: Open, High, Low, Close. All should be Dataframe.
    3. Output 1 Dataframe with 4 columns: HA_Open, HA_High, HA_Low, HA_Close.
    """
    
    # Initialize:
    HA_Open  = deepcopy(Open).values
    HA_High  = deepcopy(High).values
    HA_Low   = deepcopy(Low).values
    HA_Close = deepcopy(Close).values
    
    # Main:
    for idx in range(1, len(HA_Close)):
        HA_Close[idx] = (Open.values[idx] + High.values[idx] + Low.values[idx] + Close.values[idx]) / 4
        HA_Open [idx] = (HA_Open[idx-1] + HA_Close[idx-1]) / 2
        HA_High [idx] = max(HA_Open[idx], HA_Close[idx], High.values[idx]) 
        HA_Low  [idx] = min(HA_Open[idx], HA_Close[idx], Low.values[idx]) 
    
    HA_Open  = pd.DataFrame(HA_Open,  columns=['HA_Open'])
    HA_High  = pd.DataFrame(HA_High,  columns=['HA_High'])
    HA_Low   = pd.DataFrame(HA_Low,   columns=['HA_Low' ])
    HA_Close = pd.DataFrame(HA_Close, columns=['HA_Close']) 
    
    HA = pd.concat([HA_Open, HA_High, HA_Low, HA_Close], axis=1)
    
    return HA