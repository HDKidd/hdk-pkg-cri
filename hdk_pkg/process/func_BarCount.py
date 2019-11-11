# -*- coding: utf-8 -*-
"""
@author: He Dekun
"""

import numpy as np
import pandas as pd

def func_BarCount(HA_Open, HA_Close, HA_PS, bar_pass_cut=2, ps_pass_cut=2):
    """
    0. This function is for counting indices of continuously up or down bar (skipping some small-ps bar).
    1. This function has 5 arguments and returns 1 DataFrame with 3 colunms as output.
    2. Input arguments including: 
        (1) HA_Open, HA_Close, HA_PS, all are DataFrame.
        (2) bar_pass_cut: int, optional, default is 2, number of small opposite bars we can skip.
        (3) ps_pass_cut: int, optional, default is 2, ps cut level of oppsite bar we can skip.
    3. Output are combined in 1 DataFrame with 3 columns, including:
        (1) bar_len: HA bar trend cycle length, up trend being positive number, while down trend being negative.
        (2) bar_idx: count bar index, always starts from 1 or -1, would use future data to update current count index. (Use this carefully)
        (3) bar_idx_live: cout bar index, may start from numbers larger than 1, would not use furture data.
    """
    
    # Initialize:
    PS = HA_PS.values
    bar_len = np.zeros_like(HA_Open)
    bar_idx = np.zeros_like(HA_Open)
    bar_idx_live = np.zeros_like(HA_Open)
    
    idx_first = np.where(PS != 0)[0][0]
    bar_stats = np.zeros((len(HA_Open),3))
    bar_pass = 0
    idx = 0
    
    # Main:
    for i in range(idx_first, len(HA_Open)):
        bar_temp = np.sign(HA_Close.values[i] - HA_Open.values[i])
        # Up trend:
        if bar_temp == 1:
            if idx >= 0:
                idx += 1
                bar_stats[i, 0] = idx
                bar_idx_live[i] = idx
                bar_pass = 0
            else:
                if (PS[i] < ps_pass_cut) and (bar_pass < bar_pass_cut):
                    idx -= 1
                    bar_stats[i, 0] = idx
                    bar_idx_live[i] = idx
                    bar_pass += 1
                    if PS[i] == 0: bar_pass -= 1
                else:
                    bar_stats[i-bar_pass, 1] = idx + bar_pass
                    idx = bar_pass + 1
                    bar_stats[i, 0] = idx
                    bar_idx_live[i] = idx
                    for k in range(1, bar_pass+1): bar_stats[i-k, 0] = bar_pass + 1 - k
                    bar_pass = 0
        # Up trend:
        if bar_temp == -1:
            if idx <= 0:
                idx -= 1
                bar_stats[i, 0] = idx
                bar_idx_live[i] = idx
                bar_pass = 0
            else:
                if (PS[i] > -ps_pass_cut) and (bar_pass < bar_pass_cut):
                    idx += 1
                    bar_stats[i, 0] = idx
                    bar_idx_live[i] = idx
                    bar_pass += 1
                    if PS[i] == 0: bar_pass -= 1
                else:
                    bar_stats[i-bar_pass, 1] = idx - bar_pass
                    idx = -bar_pass - 1
                    bar_stats[i, 0] = idx
                    bar_idx_live[i] = idx
                    for k in range(1, bar_pass+1): bar_stats[i-k, 0] = -(bar_pass + 1 - k)
                    bar_pass = 0
    
    bar_stats[:, 2] = abs(bar_stats[:, 1])
    bar_idx[:] = bar_stats[:, 0]
    bar_len[:] = bar_stats[:, 2]
    
    bar_len_df      = pd.DataFrame(bar_len, columns=['bar_len'])
    bar_idx_df      = pd.DataFrame(bar_idx, columns=['bar_idx'])
    bar_idx_live_df = pd.DataFrame(bar_idx_live, columns=['bar_idx_live'])
    output_df = pd.concat([bar_len_df, bar_idx_df, bar_idx_live_df], axis=1)
    
    return output_df