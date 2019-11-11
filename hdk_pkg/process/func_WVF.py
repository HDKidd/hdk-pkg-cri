# -*- coding: utf-8 -*-
"""
@author: He Dekun
"""

import numpy as np
import pandas as pd

def func_WVF(close, low, Lookback=22):
    
    WVF = np.zeros((len(close),1))
    for i in range(Lookback, len(close)):
        highest_close_temp = close[i-22:i].max()
        WVF[i] = (1 - low.values[i] / highest_close_temp) * 100

    WVF_df = pd.DataFrame(WVF, index=close.index)
    WVF_df.columns = ['WVF']
    
    return WVF_df