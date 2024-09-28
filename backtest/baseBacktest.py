#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 19:53:46 2022

@author: vino
"""
import sys
import os
import pandas as pd
import numpy as np
#sys.path.append('/home/vino/auto_signal/')
#from strategy import CPRStrategy 
from termcolor import colored
from basePlot import candlePlot

class baseBacktest:
    
    btl=pd.DataFrame([],columns=['pair','EnL','ExL','per_gain','is_long','exit'])
    bts=pd.DataFrame([],columns=['pair','EnS','ExS','per_gain','is_short','exit'])
    verbose=True
    
    def __init__(self,df,pair):

        self.df=df
        self.pair=pair
        self.df=self.getEntryExitForBacktest(self.df,self.pair)
        self.df=self.getBacktested(self.df, self.pair)
        
        candlePlot(self.df, plot=True)

    def collect_long(self,long_details):
        baseBacktest.btl=pd.concat([baseBacktest.btl,pd.DataFrame([long_details]) ],ignore_index=True)       
    def collect_short(self,short_details):
        baseBacktest.bts=pd.concat([baseBacktest.bts,pd.DataFrame([short_details])],ignore_index=True)  
        
    def getEntryExitForBacktest(self,df,pair):
        
        #use startegy to get enry and exit for backtest
        #copy paste from #getSignal loop in CPR strategy
        #signal parameters
        
        df['candle']=99
        df['type']='NA'        
                   
        df['enter_long']=0
        df['exit_long']=0
        df['enter_short']=0
        df['exit_short']=0 
        
        df['SL']=np.nan
        df['TP']=np.nan
        
        on_long=False
        on_short=False
        
        df['exit_reason']=0          
                     
        trade_long_idx=0
        trade_short_idx=0
        
        sl_short=0
        tp_short=0
        
        sl_long=0
        tp_long=0
        timeframe='5m'
   
        ####################################################################
        ##now populate buy & sell signal based on last but 1 candle
        ##last candle is running candle. take signal based on closed candles
        ##best to have signal within 30s of candle close
        
        #i=50 will have ema50. so live candle will be 52. so start with 53 in loop.
        #so that i-1 will be live candle
        for i in range(53,len(df)):
            #latest closed candle
            lc_idx=i-2
            lc=df.iloc[lc_idx]
            
            #latest closed minus 1 candle
            lcm1_idx=i-3
            lcm1=df.iloc[lcm1_idx]
            
            #live candle
            live_idx=i-1
            lv=df.iloc[live_idx]
            
            #if live candle moves to closed candle in the meantime between signal & execution, what happens
            #it will happen only in the next pull
            #check live candle should not be in sl/tp while entering with closed candle
            #(lc['BC'] > lcm1['TC']) should be based on dat candle. but it is based on 5m candle in algo
            
            PR=1
            #signal for long
            if (#(lc['BC'] > lcm1['TC']) and\
                (lc['ema20_inc']==1 and  lc['ema50_inc']==1) and\
                #(lc['ema20_A_ema50']==1) and\
                (on_long==False)):
                            
                if( (lc['close'] > lc['TC']) and (lc['close'] < lc['R1']) ): 
                    df['SL'].iloc[live_idx]=lc['BC']
                    df['TP'].iloc[live_idx]=lc['R1']
                    sl_long=lc['BC']
                    tp_long=lc['R1']
                    
                    #print('ratio: %s'%pair,((tp_long-lv['close'])/(lv['close']-sl_long)))
                    if( ((tp_long-lv['open'])/(lv['open']-sl_long)) >= PR):                 
                        print(colored('Signal:%s, Price: %s(L1  ), pair: %16s\n'%(timeframe,lv['close'],pair),'green'))
                        df['enter_long'].iloc[live_idx]=1
                        on_long=True                
                
                elif( (lc['close'] > lc['R1']) and (lc['close'] < lc['R2']) ): 
                    df['SL'].iloc[live_idx]=lc['TC']
                    df['TP'].iloc[live_idx]=lc['R2'] 
                    sl_long=lc['TC']
                    tp_long=lc['R2']
                               
                    #print('ratio: %s'%pair,((tp_long-lv['close'])/(lv['close']-sl_long)))
                    if( ((tp_long-lv['open'])/(lv['open']-sl_long)) >= PR):                 
                        print(colored('Signal:%s, Price: %s(L1  ), pair: %16s\n'%(timeframe,lv['close'],pair),'green'))
                        df['enter_long'].iloc[live_idx]=1
                        on_long=True                  
                             
            if(on_long==True and sl_long != 0):
                   if(lv['low'] <= sl_long): 
                       on_long=False
                       df['exit_long'].iloc[live_idx]=1 
                       df['exit_reason'].iloc[live_idx]='sl'
                       
                   elif(lv['high'] >= tp_long):
                       on_long=False
                       df['exit_long'].iloc[live_idx]=1 
                       df['exit_reason'].iloc[live_idx]='tp'
                       
            # #signal for short
            # if ((lc['TC'] < lcm1['BC']) and\
            #     (lc['ema20_dec']==1 and  lc['ema50_dec']==1) and\
            #     (lc['ema20_B_ema50']==1) and\
            #     (on_short==False)):
                            
            #     if( (lc['close'] < lc['BC']) and (lc['close'] > lc['S1']) ): 
            #         sl_short=lc['TC']
            #         tp_short=lc['S1']
            #         df['SL'].iloc[live_idx]=lc['TC']
            #         df['TP'].iloc[live_idx]=lc['S1']                    

            #         if( ((lv['open']-tp_short)/(sl_short-lv['open'])) >= PR): 
         
            #             print(colored('Signal:%s, Price: %s(L1  ), pair: %16s\n'%(timeframe,lv['close'],pair),'red'))
            #             df['enter_short'].iloc[live_idx]=1
            #             on_short=True                
                
            #     elif( (lc['close'] < lc['S1']) and (lc['close'] > lc['S2']) ): 
            #         sl_short=lc['BC']
            #         tp_short=lc['S2'] 
            #         df['SL'].iloc[live_idx]=lc['BC']
            #         df['TP'].iloc[live_idx]=lc['S2']                        
           
            #         if( ((lv['open']-tp_short)/(sl_short-lv['open'])) >= PR):         
            #             print(colored('Signal:%s, Price: %s(L1  ), pair: %16s\n'%(timeframe,lv['close'],pair),'red'))
            #             df['enter_short'].iloc[live_idx]=1
            #             on_short=True                   
                             
            # if(on_short==True and sl_short != 0):
            #        if(lv['high'] >= sl_short):  
            #            on_short=False
            #            df['exit_short'].iloc[live_idx]=1  
            #            df['exit_reason'].iloc[live_idx]='sl'
            #        elif(lv['low'] <= tp_short):
            #            on_short=False
            #            df['exit_short'].iloc[live_idx]=1  
            #            df['exit_reason'].iloc[live_idx]='tp'               
        return df               
        
        
    def getBacktested(self,df,pair):
        #this back tests engulfing pull back strategy
       
        tmp=df
        EnL=np.nan
        ExL=np.nan
        EnS=np.nan
        ExS=np.nan       
                  
        is_long=False
        for i in range(len(tmp)):
                      
           #get enter long data
           #enter_long signal is printed for live candle data (-1)
           #so extry to long will be 'open' price of live candle based on last closed candle data
           if(tmp['enter_long'].iloc[i]==1 and is_long==False):
               pair=pair
               EnL=tmp['open'].iloc[i]
               is_long=True
               per_gain=0
               sl=tmp['SL'].iloc[i]
               tp=tmp['TP'].iloc[i]
               
               for j in range(i+1,len(tmp)):
                   
                   if(tmp['low'].iloc[j] <= sl and is_long==True):
                       ExL=sl
                       tmp['exit_reason'].iloc[j]='SL'
                       is_long=False
                       break
                   elif(tmp['high'].iloc[j] >= tp and is_long==True):
                       ExL=tp
                       tmp['exit_reason'].iloc[j]='TP'
                       is_long=False
                       break
                      
               if (is_long==False):        
                   per_gain=((ExL-EnL)/EnL)*100
                   exit_reason=tmp['exit_reason'].iloc[j]
                   
               if is_long==False:            
                   self.collect_long({'pair':pair,'EnL':EnL,'ExL':ExL,'per_gain':per_gain,'is_long':is_long, 'exit':exit_reason})                                               
                   
               if baseBacktest.verbose:
                   print('pair:',pair,'EnL:',EnL,'ExL:',ExL,'per_gain:',per_gain,'is_long:',is_long)

        is_short=False
        for i in range(len(tmp)):
           
           #get enter long data
           if(tmp['enter_short'].iloc[i]==1 and is_short==False):
               pair=pair
               EnS=tmp['open'].iloc[i]
               is_short=True
               per_gain=0
               sl=tmp['SL'].iloc[i]
               tp=tmp['TP'].iloc[i]    
               
               for j in range(i+1,len(tmp)):
                   if(tmp['high'].iloc[j] >= sl and is_short==True):
                       ExS=sl
                       tmp['exit_reason'].iloc[j]='SL'
                       is_short=False
                       break
                   elif(tmp['low'].iloc[j] <= tp and is_short==True):
                       ExS=tp
                       tmp['exit_reason'].iloc[j]='TP'
                       is_short=False
                       break
                                                               
               if (is_short==False):                        
                   per_gain=((EnS-ExS)/EnS)*100
                   exit_reason=tmp['exit_reason'].iloc[j]

               if is_short==False:            
                   self.collect_short({'pair':pair,'EnS':EnS,'ExS':ExS,'per_gain':per_gain,'is_short':is_short,'exit':exit_reason})  

               if baseBacktest.verbose:
                   print('pair:',pair,'EnS:',EnS,'ExS:',ExS,'per_gain:',per_gain,'is_short:',is_short)
       
        return tmp
                
    def backtestStats():
        print('#---------Backtest results for Long--------#####')
        print(baseBacktest.btl)
        print('----------------------------------------------------')
        print('Total Long: ',len(baseBacktest.btl))          
        print('Total Pass: ',len(baseBacktest.btl[baseBacktest.btl['per_gain'] > 0]))        
        print('Total Fail: ',len(baseBacktest.btl[baseBacktest.btl['per_gain'] <= 0]))
        print('Total  PnL: ',round(baseBacktest.btl['per_gain'].sum(),2))
        
        print('#---------Backtest results for Short--------#####')
        print(baseBacktest.bts)        
        print('----------------------------------------------------')
        print('Total Short: ',len(baseBacktest.bts))          
        print('Total  Pass: ',len(baseBacktest.bts[baseBacktest.bts['per_gain'] > 0]))        
        print('Total  Fail: ',len(baseBacktest.bts[baseBacktest.bts['per_gain'] <= 0]))
        print('Total  PnL: ',round(baseBacktest.bts['per_gain'].sum(),2))
        
    def stopLoss(self):
        pass
    
