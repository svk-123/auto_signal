#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 19:53:46 2022

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


class baseStrategy():
    
    def __init__(self):
        pass
    

class HAEmaStrategy(baseStrategy):
    '''
    class HAEmaStrategy
    '''
    
    def __init__(self,exchange,pair,timeframe,htimeframe,limit,plot=False,backtest=False,trade=False,dryrun=True):
        
        tmp=basePullData(exchange,pair,timeframe,htimeframe,limit,plot=False)
        
        self.df=tmp.df
        self.df_h=tmp.df_h
        self.signal=False
        
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
        df['ema10']=ta.ema(df['close'],length=10)
        df['ema20']=ta.ema(df['close'],length=20)
       
        df['rsi'] = ta.rsi(df['close'],length=14)
        df['rsi_ema'] = ta.ema(df['rsi'],length=8)
        
        df['mfi']=ta.mfi(df['high'],df['low'],df['close'],df['volume'],length=14)
        
        df['ema10_inc'] = ta.increasing(df['ema10'], length=3)
        df['ema10_dec'] = ta.decreasing(df['ema10'], length=3)
        
        df['rsi_inc'] = ta.increasing(df['rsi'], length=3, percent=1)  
        df['rsi_dec'] = ta.decreasing(df['rsi'], length=3, percent=1)
        
   
        df['candle']=99
        df['type']='NA'        
        
        #singmal
        df['ema10_A_ema20']=ta.above(df['ema10'],df['ema20'])
        df['ema10_B_ema20']=ta.below(df['ema10'],df['ema20'])
    
        df['ema_cross_A']=ta.cross(df['ema10'],df['ema20'],above=True)
        df['ema_cross_B']=ta.cross(df['ema10'],df['ema20'],above=False)
        
        df['rsi_cross_A']=ta.cross(df['rsi'],df['rsi_ema'],above=True)
        df['rsi_cross_B']=ta.cross(df['rsi'],df['rsi_ema'],above=False)
    
        df['enter_long']=0
        df['exit_long']=0
        
        df['enter_short']=0
        df['exit_short']=0  
        
        #highertimeframe df
        df_h['ema10']=ta.ema(df_h['close'],length=10)
        df_h['ema20']=ta.ema(df_h['close'],length=20)
        df_h['ema10_inc'] = ta.increasing(df_h['ema10'], length=3)
        df_h['ema10_dec'] = ta.decreasing(df_h['ema10'], length=3)
        #psar
        df[['PSARl','PSARs','PSARaf','PSARr']]=ta.psar(df['o_high'],df['o_low'],df['o_close'])
        
        for i in range(1,len(df)):
            
            
            #bull candle-green
            if(df['close'].iloc[i] >= df['open'].iloc[i]) and (df['low'].iloc[i] == df['open'].iloc[i]):
                                                                  
                df['candle'].iloc[i]=1
                df['type'].iloc[i]='green'
                
            #indicisive candle-green
            elif(df['close'].iloc[i] >= df['open'].iloc[i]) and (df['low'].iloc[i] < df['open'].iloc[i]):
                df['candle'].iloc[i]=0
                df['type'].iloc[i]='green'
                
            #bear candle-red
            elif(df['close'].iloc[i] <= df['open'].iloc[i]) and (df['high'].iloc[i] == df['open'].iloc[i]):
                df['candle'].iloc[i]=-1
                df['type'].iloc[i]='red'
                
            ##indicisive candle-red
            elif(df['close'].iloc[i] <= df['open'].iloc[i]) and (df['high'].iloc[i] >= df['open'].iloc[i]):
                df['candle'].iloc[i]=0
                df['type'].iloc[i]='red'
        ###_----------------------------------
    
        on_long=False
        on_short=False
        for i in range(len(df)):
            
            #long
            if (on_long==False and df['candle'].iloc[i] == 1 and df['ema10_A_ema20'].iloc[i] == 1): 
                df['enter_long'].iloc[i]=1
                on_long=True
                
            if (on_long==True and df['candle'].iloc[i] == -1): 
                df['exit_long'].iloc[i]=1
                on_long=False
                
            #print signal for last candle    
            if (i==len(df)-1 and df['enter_long'].iloc[i]==1):
                tmp=df['ema_cross_A'].iloc[i]
                tmp_inc=df_h['ema10_inc'].iloc[-1:]
                print(colored('Signal: Long -%3s, Time: %s(L  ), pair: %16s, EMA_Cross: %d, HTF-inc:%d\n'%(timeframe,df.index[i],pair,tmp, tmp_inc),'green'))
                self.signal=True
                
            #print signal for last-1 candle 
            if (i==len(df)-2 and df['enter_long'].iloc[i]==1):  
                tmp=df['ema_cross_A'].iloc[i]
                tmp_inc=df_h['ema10_inc'].iloc[-1:]
                print(colored('Signal: Long -%3s, Time: %s(L-1), pair: %16s, EMA_Cross: %d, HTF-inc:%d\n'%(timeframe,df.index[i],pair,tmp, tmp_inc),'green'))
                self.signal=True
                
            #short
            if (on_short==False and df['candle'].iloc[i] == -1 and df['ema10_B_ema20'].iloc[i] == 1): 
                df['enter_short'].iloc[i]=1
                on_short=True
                
            if (on_short==True and df['candle'].iloc[i] == 1): 
                df['exit_short'].iloc[i]=1
                on_short=False
                
            #print signal for last candle    
            if (i==len(df)-1 and df['enter_short'].iloc[i]==1): 
                tmp=df['ema_cross_B'].iloc[i]
                tmp_dec=df_h['ema10_dec'].iloc[-1:]                
                print(colored('Signal: Short-%3s, Time: %s(L  ), pair: %16s, EMA_Cross: %d, HTF-dec:%d\n'%(timeframe,df.index[i],pair,tmp,tmp_dec),'red'))
                self.signal=True
                
            #print signal for last-1 candle    
            if (i==len(df)-2 and df['enter_short'].iloc[i]==1):  
                tmp=df['ema_cross_B'].iloc[i]
                tmp_dec=df_h['ema10_dec'].iloc[-1:] 
                print(colored('Signal: Short-%3s, Time: %s(L-1), pair: %16s, EMA_Cross: %d, HTF-dec:%d\n'%(timeframe,df.index[i],pair,tmp,tmp_dec),'red'))            
                self.signal=True
        return df
    
    
    
class HAEmaRsiPsarStrategy(baseStrategy):
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
        
        df['rsi_inc'] = ta.increasing(df['rsi'], length=1, percent=1)  
        df['rsi_dec'] = ta.decreasing(df['rsi'], length=1, percent=1)
        
        df['rsi_cross_A']=ta.cross(df['rsi'],df['rsi_ema'],above=True)
        df['rsi_cross_B']=ta.cross(df['rsi'],df['rsi_ema'],above=False)  
        
        df['mfi']=ta.mfi(df['high'],df['low'],df['close'],df['volume'],length=14)

        df['ema10']=ta.ema(df['close'],length=10)
        df['ema20']=ta.ema(df['close'],length=20)
        df['ema50']=ta.ema(df['close'],length=50) 
        df['ema10_inc'] = ta.increasing(df['ema10'], length=1)
        df['ema10_dec'] = ta.decreasing(df['ema10'], length=1)
        
        df['ema10_A_ema20']=ta.above(df['ema10'],df['ema20'])
        df['ema10_B_ema20']=ta.below(df['ema10'],df['ema20'])
    
        df['ema_cross_A']=ta.cross(df['ema10'],df['ema20'],above=True)
        df['ema_cross_B']=ta.cross(df['ema10'],df['ema20'],above=False)

        #psar
        df[['PSARl','PSARs','PSARaf','PSARr']]=ta.psar(df['o_high'],df['o_low'],df['o_close']) 
        
        #highertimeframe df
        df_h['ema10']=ta.ema(df_h['close'],length=10)
        df_h['ema20']=ta.ema(df_h['close'],length=20)
        df_h['ema10_inc'] = ta.increasing(df_h['ema10'], length=3)
        df_h['ema10_dec'] = ta.decreasing(df_h['ema10'], length=3)
        
       
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
        for i in range(20,len(df)):
            
            #long
            if (on_long==False and 
                
                df['candle'].iloc[i] == 1 and 
                (df['PSARl'].iloc[i:i+1].isna().any() == False and df['PSARl'].iloc[i] < df['o_close'].iloc[i]) and
                #df['PSARr'].iloc[i] == 1 and
                ((df['rsi_cross_A'].iloc[i] == 1 and df['rsi'].iloc[i-1:i+1].any() < 40) or (df['rsi_cross_A'].iloc[i-1:i+1].any() == 1 and df['ema_cross_A'].iloc[i]==1)) and
                #df['rsi_cross_A'].iloc[i] == 1
                #(df['rsi'].iloc[i-1:i+1].any() < 35   and df['rsi_inc'].iloc[i]==1 )                    
                #df['ema_cross_A'].iloc[i] == 1
                #df['ema10_B_ema20'].iloc[i] == 1
                # df['ema_cross_A'].iloc[i] == 1
                (df['ema10_inc'].iloc[i]==1 or df['ema10_A_ema20'].iloc[i] == 1)
                ):
                                
                df['enter_long'].iloc[i]=1
                on_long=True
                
            #exit long    
            if (on_long==True and 
                
                (df['candle'].iloc[i] == -1 or 
                (df['PSARl'].iloc[i:i+1].isna().any() == True and df['PSARr'].iloc[i] == 1) or 
                 df['rsi_cross_B'].iloc[i] == 100)
                ): 
                df['exit_long'].iloc[i]=1
                on_long=False
                
                if(df['candle'].iloc[i] == -1):
                    df['exit_reason'].iloc[i]='candle'
                if((df['PSARl'].iloc[i:i+1].isna().any() == True and df['PSARr'].iloc[i] == 1) ):
                    df['exit_reason'].iloc[i]='psar'
                #if(df['rsi_cross_B'].iloc[i] == 1):
                #    df['exit_reason'].iloc[i]='rsi'
                                                
            #print signal for last candle    
            if (i==len(df)-1 and df['enter_long'].iloc[i]==1):
                tmp=df['ema_cross_A'].iloc[i]
                tmp_inc=df_h['ema10_inc'].iloc[-1:]
                print(colored('Signal: Long -%3s, Time: %s(L  ), pair: %16s, EMA_Cross: %d, HTF-inc:%d\n'%(timeframe,df.index[i],pair,tmp, tmp_inc),'green'))
                self.signal=True
                
            #print signal for last-1 candle 
            if (i==len(df)-2 and df['enter_long'].iloc[i]==1):  
                tmp=df['ema_cross_A'].iloc[i]
                tmp_inc=df_h['ema10_inc'].iloc[-1:]
                print(colored('Signal: Long -%3s, Time: %s(L-1), pair: %16s, EMA_Cross: %d, HTF-inc:%d\n'%(timeframe,df.index[i],pair,tmp, tmp_inc),'green'))
                self.signal=True
                
            #short
            if (on_short==False and 
                
                df['candle'].iloc[i] == -1 and 
                (df['PSARs'].iloc[i:i+1].isna().any() == False and df['PSARs'].iloc[i] > df['o_close'].iloc[i]) and
                ((df['rsi_cross_B'].iloc[i] == 1 and df['rsi'].iloc[i-1:i+1].any() > 60)  or (df['rsi_cross_B'].iloc[i-1:i+1].any() == 1 and df['ema_cross_B'].iloc[i]==1)) and
                #df['rsi_cross_B'].iloc[i] == 1   and
                (df['ema10_dec'].iloc[i]==1 or df['ema10_B_ema20'].iloc[i] == 1)
                ):    
                
                df['enter_short'].iloc[i]=1
                on_short=True
            #exit short    
            if (on_short==True and 
                
                (df['candle'].iloc[i] == 1 or 
                (df['PSARs'].iloc[i:i+1].isna().any() == True and df['PSARr'].iloc[i] == 1) or 
                 df['rsi_cross_A'].iloc[i] == 100)
                ): 
                df['exit_short'].iloc[i]=1
                on_short=False
                if(df['candle'].iloc[i] == -1):
                    df['exit_reason'].iloc[i]='candle'
                if((df['PSARs'].iloc[i:i+1].isna().any() == True and df['PSARs'].iloc[i] == 1) ):
                    df['exit_reason'].iloc[i]='psar'
                    
            #print signal for last candle    
            if (i==len(df)-1 and df['enter_short'].iloc[i]==1): 
                tmp=df['ema_cross_B'].iloc[i]
                tmp_dec=df_h['ema10_dec'].iloc[-1:]                
                print(colored('Signal: Short-%3s, Time: %s(L  ), pair: %16s, EMA_Cross: %d, HTF-dec:%d\n'%(timeframe,df.index[i],pair,tmp,tmp_dec),'red'))
                self.signal=True
                
            #print signal for last-1 candle    
            if (i==len(df)-2 and df['enter_short'].iloc[i]==1):  
                tmp=df['ema_cross_B'].iloc[i]
                tmp_dec=df_h['ema10_dec'].iloc[-1:] 
                print(colored('Signal: Short-%3s, Time: %s(L-1), pair: %16s, EMA_Cross: %d, HTF-dec:%d\n'%(timeframe,df.index[i],pair,tmp,tmp_dec),'red'))            
                self.signal=True
        return df    
    
    
    
    
   
    
    