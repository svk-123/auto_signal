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
    
class PullBackStrategy1():
    '''
    This class introduces pull back strategy of TTC
    '''
    
    def __init__(self,exchange,pair,timeframe,htimeframe,limit,plot=False,backtest=False,trade=False,dryrun=True):
        
        tmp=basePullData(exchange,pair,timeframe,htimeframe,limit,plot=False)
        
        self.df=tmp.df
        self.df_h=tmp.df_h
        self.signal=True
        self.SL = 0.02
        
        #get signals in df
        self.df=self.get_pivots(self.df)
        self.df=self.getSignal(self.df, self.df_h, timeframe, pair)
        
        if plot:
            candlePlot(self.df, plot=True)
        if backtest:
            baseBacktest(self.df,pair)
         
        if (trade==True and dryrun==True):
            baseTrade(pair,self.df,self.signal,timeframe,trade=True,dryrun=True)
            
    def get_pivots(self, df, cols=['o_open','o_high','o_low', 'o_close']):
        

        df['color']=np.nan
        df['engulf']=np.nan
        
        df['idx']=np.nan
        for i in range(len(df)):
            df['idx'].iloc[i]=i
        
        #candle color
        for i in range(1,len(df)):
            #green
            if(df['o_close'].iloc[i] >= df['o_open'].iloc[i]):
                df['color'].iloc[i]='green'
            #red    
            elif(df['o_close'].iloc[i] < df['o_open'].iloc[i]):
                df['color'].iloc[i]='red'        
        
        #engulf??
        for i in range(1,len(df)):
            #red engulf
            if(df['o_close'].iloc[i] <= df['o_open'].iloc[i-1] and df['color'].iloc[i]=='red' and df['color'].iloc[i-1]=='green'):
                
                df['engulf'].iloc[i]=1
            #green engulf
            if(df['o_close'].iloc[i] >= df['o_open'].iloc[i-1] and df['color'].iloc[i]=='green' and df['color'].iloc[i-1]=='red'):
                df['engulf'].iloc[i]=1                
                
        
        op=df['o_open']
        hi=df['o_high']
        lo=df['o_low']
        cl=df['o_close']
        
        #print('len df',len(df))
        ###########-----------------
        
        ###get all required cols populated for the strategy

        
        df['rsi'] = ta.rsi(df['o_close'],length=14)
        df['rsi_ema'] = ta.ema(df['rsi'],length=8)
        

        df['ema10']=ta.ema(df['o_close'],length=10)
        df['ema20']=ta.ema(df['o_close'],length=20)
        df['ema50']=ta.ema(df['o_close'],length=50)      
        df['ema200']=ta.ema(df['o_close'],length=100) 
        
        df['h1']=np.nan
        df['l1']=np.nan
        df['h2']=np.nan
        df['l2']=np.nan
        
        #value
        df['h1v']=np.nan
        df['l1v']=np.nan
        df['h2v']=np.nan
        df['l2v']=np.nan        
        
        #
        df['eng_up']=np.nan
        df['eng_down']=np.nan        
        
        df['grbar']=np.nan
        #check whether 123 or swing low/high (engulf or engulf-1 will have low/high)
        df['engulf_hl']=np.nan
        df['trend']=np.nan
        #check if engult does not close above/below previous low/high
        df['engulf_hl2']=np.nan
        ###########-------------------

        #df=baseCustomIndicators.highLow(self,df)
        h1=np.nan
        l1=np.nan
        h2=np.nan
        l2=np.nan
        grbar_red=np.nan
        grbar_green=np.nan
        engulf_hl=0
        engulf_hl2=0
        
        #lc - latest candle
        for lc in range(len(df)-20,len(df)):
            #get trend
            trend = 'none'
            
            if(ta.increasing(df['ema50'],length=3).iloc[lc]==1 and df['o_close'].iloc[lc] > df['ema50'].iloc[lc]):
                trend='up'
            if(ta.decreasing(df['ema50'],length=3).iloc[lc]==1 and df['o_close'].iloc[lc] < df['ema50'].iloc[lc]):
                trend='down'    
                
            #print('trend',trend)
            #print('lc',lc)
            
            #assume downtrednd
            #locate the engulf red
            #locate swing high
            #check if it is swing
            #find the previous high
            #check if new high close lower than previous high
            #check engulf bar did not close below swing low
            #gap between ema & bar
            #check if the 200 ema clasj inbetween close & TP
            
            #uptrend 
            ###----------------------------------------------------------------
            engulf=0
            if(trend=='up'):
                
                if(df['engulf'].iloc[lc]==1 and df['color'].iloc[lc]=='green'):
                    engulf=1
                #print('engulf',engulf)
                
                if(engulf==1):
                    #locate swing low
                    #here h1 indicates low

                    if(lo.iloc[lc] <= lo.iloc[lc-1]):
                        l1=lc
                    elif(lo.iloc[lc] > lo.iloc[lc-1]):
                        l1=lc-1        
                    #print('l1',l1)
                    if(np.isnan(l1)==True):
                        l1=lc
                       
                    #find swing high (previous high before engulf)
                    for i in range(2,15):
                        if(hi.iloc[l1-i] >= hi.iloc[l1-i-1] and hi.iloc[l1-i] >= hi.iloc[l1-i-2]):
                            if(hi.iloc[l1-i] >= hi.iloc[l1-i+1] and hi.iloc[l1-i] >= hi.iloc[l1-i+2]):
                                h1=l1-i
                                break
                    #print('h1',h1)        
                    if(np.isnan(h1)==True):
                        h1=lc
                        
                    #check how many green candle inbwetween swing low & engulf high
                    tmp=df['color'].iloc[h1:l1]
                    grbar_red=len(tmp[tmp=='red'])
                    #print('grbar_red',grbar_red)
                    #check the previous low
                    for i in range(2,15):
                        if(lo.iloc[h1-i] <= lo.iloc[h1-i+1] and lo.iloc[h1-i] <= lo.iloc[h1-i+2]):
                            if(lo.iloc[h1-i] <= lo.iloc[h1-i-1] and lo.iloc[h1-i] <= lo.iloc[h1-i-2]):
                                l2=h1-i
                                break        
                    #print('l2',l2)  
                    if(np.isnan(l2)==True):
                        l2=lc
                    
                    engulf_hl=1
                    #check if engulf low is valid (previous two candles are not lower)
                    #check if any lower inbetween h1 & l1
                    tmp=lo.iloc[h1:l1]
                  
                    if(len(tmp[tmp < lo.iloc[l1]]) > 0):
                        engulf_hl=0
                    #print('engulf low',engulf_hl)
                    #print('h2',h2)
                    engulf_hl2=0
                    if(cl.iloc[lc] < hi.iloc[h1]):
                        engulf_hl2=1   
                             
                    #print('rbar',rbar)
                    #append all to df
                    df['trend'].iloc[lc]=trend
                    df['h1'].iloc[lc]=h1
                    df['l1'].iloc[lc]=l1
                    df['h2'].iloc[lc]=h2
                    df['l2'].iloc[lc]=l2
                    df['grbar'].iloc[lc]=grbar_red
                    df['engulf_hl'].iloc[lc]=engulf_hl
                    df['engulf_hl2'].iloc[lc]=engulf_hl2

                    # df['h1v'].iloc[h1]=df['o_high'].iloc[h1]
                    # df['l1v'].iloc[l1]=df['o_low'].iloc[l1]
                    # df['l2v'].iloc[l2]=df['o_low'].iloc[l2]                    
           
                    df['eng_up'].iloc[lc]=1

            ###----------------------------------------------------------------
            engulf=0
            if(trend=='down'):
                
                if(df['engulf'].iloc[lc]==1 and df['color'].iloc[lc]=='red'):
                    engulf=1
                #print('engulf',engulf)
                
                if(engulf==1):
                    #locate swing high
                    
                    if(hi.iloc[lc] >= hi.iloc[lc-1]):
                        h1=lc
                    elif(hi.iloc[lc] < hi.iloc[lc-1]):
                        h1=lc-1          
                   # print('h1',h1)
                    if(np.isnan(h1)==True):
                        h1=lc
                        
                    engulf_hl=0
                    #check if engulf high is valid (previous two candles are not higher)                
                    if(hi.iloc[h1] > hi.iloc[h1-1] and hi.iloc[h1] > hi.iloc[h1-2]):
                        engulf_hl=1
                    #print('engulf high',engulf_hl)
                        
                    #find swing low (previous low before engulf)
                    for i in range(2,15):
                        if(lo.iloc[h1-i] <= lo.iloc[h1-i+1] and lo.iloc[h1-i] <= lo.iloc[h1-i+2]):
                            if(lo.iloc[h1-i] <= lo.iloc[h1-i-1] and lo.iloc[h1-i] <= lo.iloc[h1-i-2]):
                                l1=h1-i
                                break
                    #print('l1',l1)   
                    if(np.isnan(l1)==True):
                        l1=lc
                    
                    #check how many green candle inbwetween swing low & engulf high
                    tmp=df['color'].iloc[l1:h1]
                    grbar_green=len(tmp[tmp=='green'])
                    #print('gbar_green',grbar_green)
                    
                    #check the previous high
                    for i in range(2,15):
                        if(hi.iloc[l1-i] >= hi.iloc[l1-i+1] and hi.iloc[l1-i] >= hi.iloc[l1-i+2]):
                            if(hi.iloc[l1-i] >= hi.iloc[l1-i-1] and hi.iloc[l1-i] >= hi.iloc[l1-i-2]):
                                h2=l1-i
                                break        
                    #print('h2',h2)
                    if(np.isnan(l2)==True):
                        l2=lc
                    
                    engulf_hl2=0
                    if(cl.iloc[lc] > lo.iloc[l1]):
                        engulf_hl2=1
                    
                    #append all to df    
                    df['trend'].iloc[lc]=trend
                    df['h1'].iloc[lc]=h1
                    df['l1'].iloc[lc]=l1
                    df['h2'].iloc[lc]=h2
                    df['l2'].iloc[lc]=l2
                    df['grbar'].iloc[lc]=grbar_green
                    df['engulf_hl'].iloc[lc]=engulf_hl
                    df['engulf_hl2'].iloc[lc]=engulf_hl2   
                    
                    # df['h1v'].iloc[h1]=df['o_high'].iloc[h1]
                    # df['l1v'].iloc[l1]=df['o_low'].iloc[l1]
                    # df['h2v'].iloc[h2]=df['o_high'].iloc[h2]
                    
                    df['eng_down'].iloc[lc]=1
                    
            
        return df        
    
    def getSignal(self,df,df_h,timeframe,pair):
        '''
        This method populates the enter long/exit long & enter short/exit short signal.
        This has to populate the following(required for backtest & trade):
            
            1. Enter long
            2. Enter short
            3. Exit Long
            4. Exit short
            5. Stop loss
            6. take profit
            7. exit reson 
            
            df['enter_long']=0
            df['exit_long']=0
            df['enter_short']=0
            df['exit_short']=0 
            
            df['SL']=np.nan
            df['TP']=np.nan
            df['exit_reason']=0 
                        
        
        Parameters
        ----------


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
        
        #get swing low & high
        #len(df)=200
        #len(df)-1 = last candle
        #use last two candles for trade
        
        ############--------------------------------------------------------------------------------------
        #check if the last candle is live candle
        #check if the live candle data is close to full canlde / previous candle is full candle
        #
        
        for i in range(len(df)-2,len(df)):
            
            #------------------------------------------------------------------
            if(df['engulf'].iloc[i]==1 and\
                df['color'].iloc[i]=='green' and\
                #df['trend'].iloc[i]=='up' and\
                #df['engulf_hl'].iloc[i]==1 and\
                #df['engulf_hl2'].iloc[i]==1 and\
                #df['grbar'].iloc[i]>=2 and\
                np.isnan(df['l1'].iloc[i])==False and\
                on_long==False  
                ):
                    print(colored('Signal:%s, Time: %s(L1  ), pair: %16s\n'%(timeframe,df.index[i],pair),'green'))
                    df['enter_long'].iloc[i]=1
                    
                    idx=int(df['l1'].iloc[i])
                    print(i)
                    df['SL'].iloc[i]=df['o_low'].iloc[idx]
                    df['TP'].iloc[i]=(df['o_close'].iloc[i]-df['o_low'].iloc[idx])*tp_sl + df['o_close'].iloc[i]
                    on_long=True
                    trade_long_idx=i
                                                     
                    #if sl > 3%, make sl = 3%
                    if(df['SL'].iloc[i] < df['o_close'].iloc[i]*0.98):
                        df['SL'].iloc[i] = df['o_close'].iloc[i]*0.98
                    #if tp > 3%, make tp = 10%
                    if(df['TP'].iloc[i] > df['o_close'].iloc[i]*1.05):
                        df['TP'].iloc[i] = df['o_close'].iloc[i]*1.05                          
                    print('sl',df['SL'].iloc[i],'tp',df['TP'].iloc[i])

                    sl_long=df['SL'].iloc[i]
                    tp_long=df['TP'].iloc[i]
                    
            #this is valid only for backtesting
            if(on_long==True and i > trade_long_idx and sl_long != 0):
                if(df['o_low'].iloc[i] <= sl_long or df['o_high'].iloc[i] >= tp_long):
                    on_long=False
                    df['exit_long'].iloc[i]=1
                                                                     
                    
            #------------------------------------------------------------------
            
            if(df['engulf'].iloc[i]==1 and\
                df['color'].iloc[i]=='red' and\
                #df['trend'].iloc[i]=='down' and\
                #df['engulf_hl'].iloc[i]==1 and\
                #df['engulf_hl2'].iloc[i]==1 and\
                #df['grbar'].iloc[i]>=2 and\
                np.isnan(df['h1'].iloc[i])==False and\
                on_short==False
                ):    
                      print(i)
                      print(colored('Signal:%s, Time: %s(L1  ), pair: %16s\n'%(timeframe,df.index[i],pair),'red'))
                      df['enter_short'].iloc[i]=1
                      
                      idx=int(df['h1'].iloc[i])
                                            
                      df['SL'].iloc[i]=df['o_high'].iloc[idx]
                      df['TP'].iloc[i]=df['o_close'].iloc[i] - (df['o_high'].iloc[idx]-df['o_close'].iloc[i])*tp_sl
                      
                      on_short=True
                      trade_short_idx=i
                      
                      #if sl > 3%, make sl = 3%
                      if(df['SL'].iloc[i] > df['o_close'].iloc[i]*1.05):
                          df['SL'].iloc[i] = df['o_close'].iloc[i]*1.05
                      #if tp > 3%, make tp = 10%
                      if(df['TP'].iloc[i] < df['o_close'].iloc[i]*0.925):
                          df['TP'].iloc[i] = df['o_close'].iloc[i]*0.925                          
                      print('sl',df['SL'].iloc[i],'tp',df['TP'].iloc[i])
                      
                      sl_short=df['SL'].iloc[i]
                      tp_short=df['TP'].iloc[i]
                      
            #this is valid only for backtesting
            if(on_short==True and i > trade_short_idx and sl_short != 0):
                if(df['o_high'].iloc[i] >= sl_short or df['o_low'].iloc[i] <= tp_short):
                    on_short=False                        
                    df['exit_short'].iloc[i]=1
                    
              
                
        return df
