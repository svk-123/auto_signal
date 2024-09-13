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

    
class PatternStrategy():
    '''
    class HAEmaStrategy
    '''
    
    def __init__(self,exchange,pair,timeframe,htimeframe,limit,plot=False,backtest=False,trade=False,dryrun=True):
        
        tmp=basePullData(exchange,pair,timeframe,htimeframe,limit,plot=False)
        
        self.df=tmp.df
        self.df_h=tmp.df_h
        self.signal=False
        self.SL = 0.02
        
        #get signals in df
        self.df=self.getSignal(self.df, self.df_h, timeframe, pair)
        
        if plot:
            candlePlot(self.df, plot=True)
        if backtest:
            baseBacktest(self.df,pair)
         
        if (trade==True and dryrun==True):
            baseTrade(pair,self.df,self.signal,timeframe,trade=True,dryrun=True)
            
            
            
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

        
        df['rsi'] = ta.rsi(df['close'],length=14)
        df['rsi_ema'] = ta.ema(df['rsi'],length=8)
        

        df['ema10']=ta.ema(df['close'],length=10)
        df['ema20']=ta.ema(df['close'],length=20)
        df['ema50']=ta.ema(df['close'],length=50)         
        #get pattern
        
        df_pattern = df.ta.cdl_pattern(name="all")
        
               
        #signal
        df['candle']=99
        df['type']='NA'        
                   
        df['enter_long']=0
        df['exit_long']=0
        
        df['enter_short']=0
        df['exit_short']=0  
        
        df['exit_reason']=0          
             
        for i in range(1,len(df)):
            
            
            # #bull candle-green (strict HA)
            # if(df['close'].iloc[i] >= df['open'].iloc[i]) and (df['low'].iloc[i] == df['open'].iloc[i]):
                                                                  
            #     df['candle'].iloc[i]=1
            #     df['type'].iloc[i]='green'
                
            # #indicisive candle-green
            # elif(df['close'].iloc[i] >= df['open'].iloc[i]) and (df['low'].iloc[i] < df['open'].iloc[i]):
            #     df['candle'].iloc[i]=0
            #     df['type'].iloc[i]='green'
                
            # #bear candle-red
            # elif(df['close'].iloc[i] <= df['open'].iloc[i]) and (df['high'].iloc[i] == df['open'].iloc[i]):
            #     df['candle'].iloc[i]=-1
            #     df['type'].iloc[i]='red'
                
            # ##indicisive candle-red
            # elif(df['close'].iloc[i] <= df['open'].iloc[i]) and (df['high'].iloc[i] >= df['open'].iloc[i]):
            #     df['candle'].iloc[i]=0
            #     df['type'].iloc[i]='red'
        # ##_----------------------------------


            #bull candle-green (3% tolerance)
            f=0.03
            if(df['close'].iloc[i] >= df['open'].iloc[i]) and ((df['open'].iloc[i]-df['low'].iloc[i]) <= f*(df['high'].iloc[i]-df['open'].iloc[i])):
                                                                  
                df['candle'].iloc[i]=1
                df['type'].iloc[i]='green'
                
            #indicisive candle-green
            elif(df['close'].iloc[i] >= df['open'].iloc[i]) and ((df['open'].iloc[i]-df['low'].iloc[i]) > f*(df['high'].iloc[i]-df['open'].iloc[i])):
                df['candle'].iloc[i]=0
                df['type'].iloc[i]='green'
                
            #bear candle-red
            elif(df['close'].iloc[i] <= df['open'].iloc[i]) and ((df['high'].iloc[i]-df['open'].iloc[i]) <= f*(df['open'].iloc[i]-df['low'].iloc[i])):
                df['candle'].iloc[i]=-1
                df['type'].iloc[i]='red'
                
            ##indicisive candle-red
            elif(df['close'].iloc[i] <= df['open'].iloc[i]) and ((df['high'].iloc[i]-df['open'].iloc[i]) > f*(df['open'].iloc[i]-df['low'].iloc[i])):
                df['candle'].iloc[i]=0
                df['type'].iloc[i]='red'
        # ###_----------------------------------
    
        on_long=False
        on_short=False
        
        for i in range(20, len(df)):

            #long
            if (df_pattern['CDL_HAMMER'].iloc[i] == 100

                    ):

                df['enter_long'].iloc[i] = 1
                on_long = True

            # #exit long
            # if (on_long == True and


            #     ):
            #     df['exit_long'].iloc[i] = 1
            #     on_long = False

        return df
