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

class baseBacktest:
    
    btl=pd.DataFrame([],columns=['pair','EnL','ExL','per_gain','is_long','exit'])
    bts=pd.DataFrame([],columns=['pair','EnS','ExS','per_gain','is_short','exit'])
    verbose=False
    
    def __init__(self,df,pair):
        
        df=df
        pair=pair
        self.getBacktestedPullback(df,pair)

    def collect_long(self,long_details):
        baseBacktest.btl=baseBacktest.btl.append(long_details,ignore_index=True)
        
    def collect_short(self,short_details):
        baseBacktest.bts=baseBacktest.bts.append(short_details,ignore_index=True) 
        
    def getBacktested(self,df,pair):

        
        tmp=df[(df['enter_long']==1) | (df['exit_long']==1) | (df['enter_short']==1) |\
                  (df['exit_short']==1)]    
        
            
        is_long=False
        for i in range(len(tmp)):
            
            #get enter long data
            if(tmp['enter_long'].iloc[i]==1 and is_long==False):
                pair=pair
                EnL=tmp['o_close'].iloc[i]
                is_long=True
                per_gain=0
                
                for j in range(i,len(tmp)):
                    if(tmp['exit_long'].iloc[j]==1 and is_long==True):
                        ExL=tmp['o_close'].iloc[j]
                        if(tmp['exit_reason'].iloc[j]=='psar'):
                            ExL=tmp['o_open'].iloc[j]                        
                        is_long=False
                        per_gain=((ExL-EnL)/EnL)*100
                        if(per_gain < -3.0):
                            per_gain=-3
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
                EnS=tmp['o_close'].iloc[i]
                is_short=True
                per_gain=0
                
                for j in range(i,len(tmp)):
                    if(tmp['exit_short'].iloc[j]==1 and is_short==True):
                        ExS=tmp['o_close'].iloc[j]
                        is_short=False
                        per_gain=((EnS-ExS)/EnS)*100
                        exit_reason=tmp['exit_reason'].iloc[j]
                        if(per_gain < -3.0):
                            per_gain=-3
                if is_short==False:            
                    self.collect_short({'pair':pair,'EnS':EnS,'ExS':ExS,'per_gain':per_gain,'is_short':is_short,'exit':exit_reason})  

                if baseBacktest.verbose:
                    print('pair:',pair,'EnS:',EnS,'ExS:',ExS,'per_gain:',per_gain,'is_short:',is_short)

    def getBacktestedPullback(self,df,pair):
        #this back tests engulfing pull back strategy
        
        tmp=df    
        
            
        is_long=False
        for i in range(len(tmp)):
            
            #get enter long data
            if(tmp['enter_long'].iloc[i]==1 and is_long==False):
                pair=pair
                EnL=tmp['o_close'].iloc[i]
                is_long=True
                per_gain=0
                sl=tmp['SL'].iloc[i]
                tp=tmp['TP'].iloc[i]
                
                for j in range(i+1,len(tmp)):
                    
                    if(tmp['o_low'].iloc[j] <= sl and is_long==True):
                        ExL=sl
                        tmp['exit_reason'].iloc[j]='SL'
                        is_long=False
                        break
                    elif(tmp['o_high'].iloc[j] >= tp and is_long==True):
                        ExL=tp
                        tmp['exit_reason'].iloc[j]='TP'
                        is_long=False
                        break
                       
                        
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
                EnS=tmp['o_close'].iloc[i]
                is_short=True
                per_gain=0
                sl=tmp['SL'].iloc[i]
                tp=tmp['TP'].iloc[i]    
                
                for j in range(i+1,len(tmp)):
                    if(tmp['o_high'].iloc[j] >= sl and is_short==True):
                        ExS=sl
                        tmp['exit_reason'].iloc[j]='SL'
                        is_short=False
                        break
                    elif(tmp['o_low'].iloc[j] <= tp and is_short==True):
                        ExS=tp
                        tmp['exit_reason'].iloc[j]='TP'
                        is_short=False
                        break
                                         
                        
                        
                per_gain=((EnS-ExS)/EnS)*100
                exit_reason=tmp['exit_reason'].iloc[j]

                if is_short==False:            
                    self.collect_short({'pair':pair,'EnS':EnS,'ExS':ExS,'per_gain':per_gain,'is_short':is_short,'exit':exit_reason})  

                if baseBacktest.verbose:
                    print('pair:',pair,'EnS:',EnS,'ExS:',ExS,'per_gain:',per_gain,'is_short:',is_short)
                    
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
    
