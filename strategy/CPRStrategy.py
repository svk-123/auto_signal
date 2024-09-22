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
   
class CPRStrategy(baseStrategy):
    
    '''
    class CPRStrategy
    '''
    
    def __init__(self,exchange,pair,timeframe,htimeframe,limit,plot=False,backtest=False,trade=False,dryrun=True):
        
        tmp=basePullData(exchange,pair,timeframe,htimeframe,limit,plot=False)
        
        self.df=tmp.df
        self.df_h=tmp.df_h
        self.signal=True
        
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
        df['ema20']=ta.ema(df['close'],length=20)
        df['ema50']=ta.ema(df['close'],length=50)
        df['ema20_inc'] = ta.increasing(df['ema20'], length=5)
        df['ema50_inc'] = ta.increasing(df['ema50'], length=5)
        df['ema20_dec'] = ta.decreasing(df['ema20'], length=5)
        df['ema50_dec'] = ta.decreasing(df['ema50'], length=5)
        
        df['ema20_A_ema50']=ta.above(df['ema20'],df['ema50'])
        df['ema20_B_ema50']=ta.below(df['ema20'],df['ema50'])
        df['ema_cross_A']=ta.cross(df['ema20'],df['ema50'],above=True)
        df['ema_cross_B']=ta.cross(df['ema20'],df['ema50'],above=False)
        
        
        def getCPR(df_tmp):          
            df_tmp['pivot']=(df_tmp['high']+df_tmp['low']+df_tmp['close'])/3
            df_tmp['BC']=(df_tmp['high']+df_tmp['low'])/2           
            df_tmp['TC']=(df_tmp['pivot']-df_tmp['BC'])+df_tmp['pivot']
            df_tmp['S1']=(2*df_tmp['pivot'])-df_tmp['high']
            df_tmp['R1']=(2*df_tmp['pivot'])-df_tmp['low']
            df_tmp['S2']=df_tmp['pivot']-(df_tmp['high']-df_tmp['low'])
            df_tmp['R2']=df_tmp['pivot']+(df_tmp['high']-df_tmp['low'])           
            
            return df_tmp
        df_h=getCPR(df_h)
        
        
        ###pivots are calculated based on previous day candles.
        ###hence offset date +1 to match yesterday pivots with today's 5m chart
        
        tmp=df_h[['date','pivot','BC','TC','S1','S2','R1','R2']]
        tmp['date']=tmp['date']+pd.DateOffset(1)
        df=pd.merge(df,tmp,on='date',how='left')
        df['time']=pd.to_datetime(df['o_time'],unit='ms')
        df=df.set_index('time') 
          
        #signal parameters
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
   
   
        ####################################################################
        ##now populate buy & sell signal based on last but 1 candle
        ##last candle is running candle. take signal based on closed candles
        ##best to have signal within 30s of candle close
        
        #latest closed candle
        lc=df.iloc[-2]
        #latest closed minus 1 candle
        lcm1=df.iloc[-3]
        #live candle
        lv=df.iloc[-1]
        
        #if live candle moves to closed candle in the meantime between signal & execution, what happens
        #it will happen only in the next pull
        #check live candle should not be in sl/tp while entering with closed candle
        
        #signal for long
        if (#(lc['BC'] > lcm1['TC']) and\
            #(lc['ema20_inc']==1 and  lc['ema50_inc']==1) and\
            #(lc['ema20_A_ema50']==1) and\
            (on_long==False)):
                        
            if( (lc['close'] > lc['TC']) and (lc['close'] < lc['R1']) ): 
                sl_long=lc['BC']
                tp_long=lc['R1']
                                
                print(colored('Signal:%s, Price: %s(L1  ), pair: %16s\n'%(timeframe,lv['close'],pair),'green'))
                df['enter_long'].iloc[-1]=1
                on_long=True                
            
            elif( (lc['close'] > lc['R1']) and (lc['close'] < lc['R2']) ): 
                sl_long=lc['TC']
                tp_long=lc['R2'] 
                
                print(colored('Signal:%s, Price: %s(L1  ), pair: %16s\n'%(timeframe,lv['close'],pair),'green'))
                df['enter_long'].iloc[-1]=1
                on_long=True                  
                         
        if(on_long==True and sl_long != 0):
               if(lv['close'] <= sl_long or lv['close'] >= tp_long):
                   on_long=False
                   df['exit_long'].iloc[-1]=1            

        #signal for shprt
        if (#(lc['TC'] < lcm1['BC']) and\
            #(lc['ema20_dec']==1 and  lc['ema50_dec']==1) and\
            #(lc['ema20_B_ema50']==1) and\
            (on_short==False)):
                        
            if( (lc['close'] < lc['BC']) and (lc['close'] > lc['S1']) ): 
                sl_short=lc['TC']
                tp_short=lc['S1']
                print('ratio: %s'%pair,((lv['close']-tp_short)/(sl_short-lv['close'])))
                if( ((lv['close']-tp_short)/(sl_short-lv['close'])) >= 1.8): 
     
                    print(colored('Signal:%s, Price: %s(L1  ), pair: %16s\n'%(timeframe,lv['close'],pair),'red'))
                    df['enter_short'].iloc[-1]=1
                    on_short=True                
            
            elif( (lc['close'] < lc['S1']) and (lc['close'] > lc['S2']) ): 
                sl_short=lc['TC']
                tp_short=lc['S2'] 
                print('ratio: %s'%pair,((lv['close']-tp_short)/(sl_short-lv['close'])))               
                if( ((lv['close']-tp_short)/(sl_short-lv['close'])) >= 1.8): 
     
                    print(colored('Signal:%s, Price: %s(L1  ), pair: %16s\n'%(timeframe,lv['close'],pair),'red'))
                    df['enter_short'].iloc[-1]=1
                    on_short=True                   
                         
        if(on_short==True and sl_short != 0):
               if(lv['close'] >= sl_short):  
                   on_short=False
                   df['exit_short'].iloc[-1]=1  
                   df['exit_reason'].iloc[-1]='sl'
               elif(lv['close'] <= tp_short):
                   on_short=False
                   df['exit_short'].iloc[-1]=1  
                   df['exit_reason'].iloc[-1]='tp'                  
        return df
    
    
    

    
    
    
    
   
    
    