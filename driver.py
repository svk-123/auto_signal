#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 19:53:46 2022

@author: vino
"""
import sys
import os
import schedule 
from matplotlib import pyplot as plt
import time
import pandas as pd
pd.set_option('display.max_rows',50)
pd.set_option('display.max_columns',20)
pd.set_option("display.precision", 8)
#------from package(dir.) import class
from config import kcf_pairs_stable8,kcf_pairs_stable100, kcf_pairs_SR
from exchangeRelated import baseExchange
from pullData import basePullData
from strategy import HAEmaStrategy, HAEmaRsiPsarStrategy, PatternStrategy, PullBackStrategy1, BreakoutStrategy1
from backtest import baseBacktest
from basePlot import candlePlot
from baseTrade import baseTrade
#--------------------------------

exchange=baseExchange().getExchange()
#pairs=kcf_pairs_SR()
pairs=kcf_pairs_stable100()
#pairs=['MATIC/USDT:USDT']

######-------------------------------------------------------------------------
######-----------------------------Driver for Trade----------------------------
######-------------------------------------------------------------------------

def scan_pairs():
    
    print('Scaning pairs')
    for i in range(50):

        p1=PullBackStrategy1(exchange=exchange,
                          pair=pairs[i],
                          timeframe='1h',
                          htimeframe='4h',
                          limit=200,
                          plot=False,
                          backtest=False,
                          trade=True,
                          dryrun=True
                          )
    print('-----------------Live Trade Status-------------------') 
    print(baseTrade.liveTrade)
    print('------------------------------------------------')
    
    print('-----------------Hist Trade Status-------------------')    
    print(baseTrade.histTrade)
    print('------------------------------------------------')

    return p1
  


schedule.every(30).seconds.do(scan_pairs)

while True:
    schedule.run_pending()
    time.sleep(1)
 
######-------------------------------------------------------------------------
######-----------------------------Driver for Test/Backtest--------------------
######-------------------------------------------------------------------------

# for i in range(10):
#     print(pairs[i])    
#     p1=BreakoutStrategy1(exchange=exchange,
#                           pair=pairs[i],
#                           timeframe='15m',
#                           htimeframe='4h',
#                           limit=200,
#                           plot=True,
#                           backtest=False,
#                           trade=False,
#                           dryrun=True
#                           ) 
    
    
# # #print backtest stats    
# baseBacktest.backtestStats()
# candlePlot.plotShaprpe(baseBacktest.btl)
# candlePlot.plotShaprpe(baseBacktest.bts)

# btl=baseBacktest.btl
# #profit
# print('No of Profit: Candle',len(btl[(btl['per_gain'] > 0) & (btl['exit'] == 'candle')]))
# print('Profit: Candle',btl[(btl['per_gain'] > 0) & (btl['exit'] == 'candle')]['per_gain'].sum())
# print('No of Profit: psar',len(btl[(btl['per_gain'] > 0) & (btl['exit'] == 'psar')]))
# print('Profit: psar',btl[(btl['per_gain'] > 0) & (btl['exit'] == 'psar')]['per_gain'].sum())

# print('No of loss: Candle',len(btl[(btl['per_gain'] < 0) & (btl['exit'] == 'candle')]))
# print('loss: Candle',btl[(btl['per_gain'] < 0) & (btl['exit'] == 'candle')]['per_gain'].sum())
# print('No of loss: psar',len(btl[(btl['per_gain'] < 0) & (btl['exit'] == 'psar')]))
# print('loss: psar',btl[(btl['per_gain'] < 0) & (btl['exit'] == 'psar')]['per_gain'].sum())

# print('No of loss: Candle',len(btl[(btl['per_gain'] < 0) & (btl['exit'] == 'candle')]))
# print('No of loss: psar',len(btl[(btl['per_gain'] < 0) & (btl['exit'] == 'candle')]))

''' 
Enable live trade visualization while running by pair
display each pair with Entry, SL, TP, etc
Interative GUI

Verify pulled data is latest data by curunt time
verify trade taken before candle close as option
Give last few mins for opening the trade before candle close
'''
