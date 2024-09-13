#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 19:53:46 2022

@author: vino
"""
import sys
import os
import pandas_ta as ta
import pandas as pd
import numpy as np

class baseCustomIndicators:
    
    def __init__(self):
        pass
    
    def WaveTrend(self, df_tmp, chlen=9, avg=9, smalen=4):
        """
        WaveTrend Ocillator by LazyBear
        https://www.tradingview.com/script/2KE8wTuF-Indicator-WaveTrend-Oscillator-WT/
        """
        
        df_tmp['hlc3'] = (df_tmp['high'] + df_tmp['low'] + df_tmp['close']) / 3
        df_tmp['esa'] = ta.ema(df_tmp['hlc3'], timeperiod=chlen)
        df_tmp['d'] = ta.ema((df_tmp['hlc3'] - df_tmp['esa']).abs(), timeperiod=chlen)
        df_tmp['ci'] = (df_tmp['hlc3'] - df_tmp['esa']) / (0.015 * df_tmp['d'])
        df_tmp['tci'] = ta.ema(df_tmp['ci'], timeperiod=avg)
    
        df_tmp['wt1'] = df_tmp['tci']
        df_tmp['wt2'] = ta.sma(df_tmp['wt1'], timeperiod=smalen)
        df_tmp['wt1-wt2'] = df_tmp['wt1'] - df_tmp['wt2'] 
        
        return df_tmp
        
    def highLow(self,df):
        #get high & low (1st & 2nd ) for each candle
        
        op=df['o_open']
        hi=df['o_high']
        lo=df['o_low']
        cl=df['o_close']
        # number of candle inbetween to find high/low (with color)
        #without including the high & low candle
        df['h1']=np.nan
        df['h2']=np.nan
        df['l1']=np.nan
        df['l2']=np.nan
                
        #number of candles required with color for high/low
        df['sl']=np.nan
        for i in range(len(df)):
            df['sl'].iloc[i]=i
            
        Nc=2
        
        for i in range(101,len(df)):
            #check if candle high
            tmp=hi.iloc[i-5:i+1].idxmax()
            print(df['sl'].loc[tmp])

        for i in range(101,len(df)):
            #check if candle high
            tmp=lo.iloc[i-5:i+1].idxmin()
            


        
        #         engulf_high=0
        #         #check if engulf high is valid (previous two candles are not higher)                
        #         if(hi.iloc[h1] > hi.iloc[-l-2] and hi.iloc[h1] > hi.iloc[-l-3]):
        #             engulf_high=1
        #         print('engulf high',engulf_high)
                    
        #         #find swing low (previous low before engulf)
        #         for i in range(3,10):
        #             if(lo.iloc[-i-1] > lo.iloc[-i] and lo.iloc[-i-2] > lo.iloc[-i]):
        #                 if(lo.iloc[-i+1] > lo.iloc[-i] and lo.iloc[-i+2] > lo.iloc[-i]):
        #                     l1=-i
        #                     break
        #         print('l1',l1)        
        #         #check how many green candle inbwetween swing low & engulf high
        #         tmp=df['color'].iloc[l1:-1]
        #         gbar=len(tmp[tmp=='green'])
             
        #         #check the previous high
        #         for i in range(abs(l1),abs(l1)+10):
        #             if(hi.iloc[-i-1] <= hi.iloc[-i] and hi.iloc[-i-2] <= hi.iloc[-i]):
        #                 if(hi.iloc[-i+1] <= hi.iloc[-i] and hi.iloc[-i+2] <= hi.iloc[-i]):
        #                     h2=-i
        #                     break        
        #         print('h2',h2)     
        
        # #uptrend  
        # engulf=0
        # if(trend=='up'):
        #     print('trend',trend)
        #     if(df['engulf'].iloc[-1]==1 and df['color'].iloc[-1]=='green'):
        #         engulf=1
        #     print('engulf',engulf)
            
        #     if(engulf==1):
        #         #locate swing low
        #         #here h1 indicates low
        #         l=1
        #         if(lo.iloc[-l] < lo.iloc[-l-1]):
        #             l1=-l
        #         elif(lo.iloc[-l] > lo.iloc[-l-1]):
        #             l1=-l-1           
        #         print('l1',l1)
                
                   
        #         #find swing high (previous high before engulf)
        #         for i in range(3,10):
        #             if(hi.iloc[-i-1] < hi.iloc[-i] and hi.iloc[-i-2] < hi.iloc[-i]):
        #                 if(hi.iloc[-i+1] < hi.iloc[-i] and hi.iloc[-i+2] < hi.iloc[-i]):
        #                     h1=-i
        #                     break
        #         print('h1',h1)        
        #         #check how many green candle inbwetween swing low & engulf high
        #         tmp=df['color'].iloc[h1:-1]
        #         rbar=len(tmp[tmp=='red'])
             
        #         #check the previous high
        #         for i in range(abs(h1),abs(h1)+10):
        #             if(lo.iloc[-i-1] >= lo.iloc[-i] and lo.iloc[-i-2] >= lo.iloc[-i]):
        #                 if(lo.iloc[-i+1] >= lo.iloc[-i] and lo.iloc[-i+2] >= lo.iloc[-i]):
        #                     l2=-i
        #                     break        
        #         print('l2',l2)  
                
                
        #         engulf_low=1
        #         #check if engulf low is valid (previous two candles are not lower)
        #         #check if any lower inbetween h1 & l1
        #         tmp=lo.iloc[h1:l1]
              
        #         if(len(tmp[tmp < lo.iloc[l1]]) > 0):
        #             engulf_low=0
        #         print('engulf low',engulf_low)
                                                
        #         print('rbar',rbar)
                
        return df               
        
        