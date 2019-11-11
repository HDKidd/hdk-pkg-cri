# -*- coding: utf-8 -*-
"""
@author: He Dekun
"""

import matplotlib.pyplot as plt
import mpl_finance as mpf

def func_plot_type1(Open, High, Low, Close, indicator, result):
    
    plt.figure()
    
    # ax1
    ax1 = plt.subplot(211)
    mpf.candlestick2_ohlc(ax1, Open, High, Low, Close, width=0.5, colorup='green', colordown='red')
    
#    x = list(range(len(data_HA)))
#    y = data_HA.HA_High.values
#    p = data_PS.values  # data_CT.values
#    q = data_CT.bar_idx_live.values
    
#    for i,j in zip(x,y):
#        ax1.text(i,j, '%d' % p[i])
#        ax1.text(i,j-20, '%d' % q[i])
    
    ax1.fill_between(range(len(Close)), [Close.max()]*len(Close), [Close.min()]*len(Close),
                     where=indicator== 1, facecolor='green', alpha=0.5)
    ax1.fill_between(range(len(Close)), [Close.max()]*len(Close), [Close.min()]*len(Close),
                     where=indicator==-1, facecolor='red', alpha=0.5)

    # ax2
    ax2 = plt.subplot(212, sharex=ax1)
    plt.plot(result[0])
    plt.title('Accumulated Return = %s ; Trade Number = %s ; Return per Trade= %s bp' % (result[0][-1], result[1], result[0][-1]/result[1]*10000))
    plt.show()