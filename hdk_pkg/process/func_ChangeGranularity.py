# -*- coding: utf-8 -*-
"""
@author: He Dekun
"""

import pandas as pd

def func_ChangeGranularity(data_1min, granularity):
#    data_1min.index = pd.DatetimeIndex(data_1min.index)
#    ohlc_dict = {'open':'first', 'high':'max', 'low':'min', 'close': 'last', 'volume':'sum'}
#    return data_1min.resample('%sT' % granularity, how=ohlc_dict, closed='right', label='right')

    data_1min.index = pd.DatetimeIndex(data_1min.index)
    ohlc_dict = {'open':'first', 'high':'max', 'low':'min', 'close': 'last', 'volume':'sum'}
    return data_1min.resample('%sT' % granularity, closed='right', label='right').apply(ohlc_dict)
