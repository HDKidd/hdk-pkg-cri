# -*- coding: utf-8 -*-
"""
@author: He Dekun
"""

import pandas as pd

def func_Momentum(data_PS, data_CT):
        
    indicator = pd.concat([data_PS, data_CT], axis=1)
    indicator['indicator'] = 0
    indicator['buy_sell_type'] = 0
    indicator = indicator.values  # PS. CT. indicators, type
                                  # 0    1      2         3

    for i in range(2, len(indicator)):
        indicator[i,2] = indicator[i-1,2]
    
        # Close Long
        if (indicator[i-1,2]== 1):
            if (indicator[i,0]==-4):  # type -1: 
                indicator[i,2] = 0
                indicator[i,3] = -1
            if (indicator[i,1]<=-4):  # type -2: 
                indicator[i,2] = 0
                indicator[i,3] = -2       
        # Close Short
        if (indicator[i-1,2]==-1):
            if (indicator[i,0]== 4):  # type 1
                indicator[i,2] = 0
                indicator[i,3] = 1
            if (indicator[i,1]>=4) :  # type 2
                indicator[i,2] = 0
                indicator[i,3] = 2
        # Open Long
        if (indicator[i-1,2]!= 1):
            if (indicator[i,0]== 4):  # type 1
                indicator[i,2] = 1
                indicator[i,3] = 1
            if (indicator[i,1]>=4):  # type 2
                indicator[i,2] = 1
                indicator[i,3] = 2
        # Open Short
        if (indicator[i-1,2]!=-1):
            if (indicator[i,0]== -4):  # type -1
                indicator[i,2] = -1
                indicator[i,3] = -1
            if (indicator[i,1]<=-4):  # type -2
                indicator[i,2] = -1
                indicator[i,3] = -2
    
    return indicator