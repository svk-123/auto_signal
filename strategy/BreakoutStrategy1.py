#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 12:06:09 2022

@author: vino
"""

import sys
import os
from termcolor import colored
import numpy as np
import pandas_ta as ta
import pandas as pd
#------from package(dir.) import class
from pullData import basePullData
from basePlot import candlePlot
from backtest import baseBacktest
from baseTrade import baseTrade
from customIndicators import baseCustomIndicators
    
class BreakoutStrategy1():
    '''
    This class introduces breakout strategy 1:
        -look for close run of ema 200, 50, 20
        - look for a candle taing over previous 20 candles
        - writtedn for 15 mins data to check
    '''
    
    def __init__(self,exchange,pair,timeframe,htimeframe,limit,plot=False,backtest=False,trade=False,dryrun=True):
        
        tmp=basePullData(exchange,pair,timeframe,htimeframe,limit,plot=False)
        
        self.df=tmp.df
        self.df_h=tmp.df_h
        self.signal=False
        self.SL = 0.02
        
        #get signals in df
        self.df=self.get_calc(self.df)
        self.df=self.getSignal(self.df, self.df_h, timeframe, pair)
        
        if plot:
            candlePlot(self.df, plot=True)
        if backtest:
            baseBacktest(self.df,pair)
         
        if (trade==True and dryrun==True):
            baseTrade(pair,self.df,self.signal,timeframe,trade=True,dryrun=True)
            
    def get_calc(self, df, cols=['o_open','o_high','o_low', 'o_close']):
        
        #get lower low
                
        df['rsi'] = ta.rsi(df['o_close'],length=14)
        df['rsi_ema'] = ta.ema(df['rsi'],length=8)
        

        df['ema10']=ta.ema(df['o_close'],length=10)
        df['ema20']=ta.ema(df['o_close'],length=20)
        df['ema50']=ta.ema(df['o_close'],length=50)      
        df['ema200']=ta.ema(df['o_close'],length=200)     
        
        df['ema20h']=ta.ema(df['o_high'],length=20)
        df['ema50h']=ta.ema(df['o_high'],length=50)         
         
        
        df['ema20l']=ta.ema(df['o_low'],length=20)
        df['ema50l']=ta.ema(df['o_low'],length=50)           


        #angle of ema 
        #mean of 
        
        df['min20']=np.nan
        df['max20']=np.nan     
        df['meanhl20']=np.nan
        df['stdhl20']=np.nan
        df['ema20_mstd']=np.nan
        df['ema20_pstd']=np.nan        
        
        N=20
        
        for i in range(N+1,len(df)):
            df['max20'].iloc[i]=df['o_high'].iloc[i-20:i].max()
            df['min20'].iloc[i]=df['o_low'].iloc[i-20:i].min()            
            df['meanhl20'].iloc[i]=(df['o_high'].iloc[i-20:i]-df['o_low'].iloc[i-20:i]).mean()     
            df['stdhl20'].iloc[i]=(df['o_high'].iloc[i-20:i]-df['o_low'].iloc[i-20:i]).std()        
        
        df['ema20_mstd']=df['ema20']-df['stdhl20']
        df['ema20_pstd']=df['ema20']+df['stdhl20']        
        
        for lc in range(201,len(df)):
            pass
        
        
                    
            
        return df        
    
    def getSignal(self,df,df_h,timeframe,pair):
        '''
        This method populates the enter long/exit long & enter short/exit short signal.
        This method (specific to HAEmaStrategy) also populates the bull & bear HA candle.

        Parameters
        ----------
        df : TYPE
            DESCRIPTION.
        df_h : TYPE
            DESCRIPTION.
        timeframe : TYPE
            DESCRIPTION.
        pair : TYPE
            DESCRIPTION.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        '''
        
        
        ###get all required cols populated for the strategy
      
               
        #signal
        df['candle']=99
        df['type']='NA'        
                   
        df['enter_long']=0
        df['exit_long']=0
        df['enter_short']=0
        df['exit_short']=0 
        
        df['SL']=np.nan
        df['TP']=np.nan
        
        df['exit_reason']=0          
             
    
        on_long=False
        on_short=False
        
        trade_long_idx=0
        trade_short_idx=0
        
        sl_short=0
        tp_short=0
        
        sl_long=0
        tp_long=0
        
        tp_sl=1.5
        
                    
              
                
        return df
