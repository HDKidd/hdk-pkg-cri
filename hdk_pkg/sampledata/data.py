# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 12:52:29 2019

@author: Homiex - HDK
"""

import os
import pandas as pd

def data():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eth_kline.csv')
    return pd.read_csv(path, index_col=0)