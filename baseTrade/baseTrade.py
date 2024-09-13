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
pd.set_option('display.max_rows',50)
pd.set_option('display.max_columns',20)

class baseTrade:
    #bug base trade is called only when ther eis signal in L-1
    #so there is a probel with watching the live trades and updateing it
    liveTrade=pd.DataFrame([],columns=['pair','tF','En','Ex','per_gain','L_or_S','order_status','Exit'])
    histTrade=pd.DataFrame([],columns=['pair','tF','En','Ex','per_gain','L_or_S','order_status','Exit'])
    
    def __init__(self,pair,df,signal=False,timeframe='1h',trade=False,dryrun=True):
        pair=pair
        df=df
        timeframe=timeframe
        signal=signal
        
        if(dryrun==True and signal == True):
            if pair not in baseTrade.liveTrade['pair'].to_numpy() and len(baseTrade.liveTrade) < 5:
                self.checkEntry(pair,df,timeframe)
        
        #call watch trade only if pair in livepairs                
        if(len(baseTrade.liveTrade) > 0):
            if pair in baseTrade.liveTrade['pair'].to_numpy():
                self.watchtrade(pair,df)
                self.movetrade(pair)
                
    def checkEntry(self,pair,df,timeframe):
        # check for enter signal in the last & last -1 candle
        bl=baseTrade.liveTrade
               
        if(df['enter_long'].iloc[-2] == 1):
            print('Pair: %s Entering Long at: %5f'%(pair,df['o_close'].iloc[-1])) 
            bl=bl.append({'pair':pair,'tF':timeframe,'En':df['o_close'].iloc[-1],
                          'Ex':0,'per_gain':0,'L_or_S':'long','order_status':'C','Exit':'open'},ignore_index=True)
            
        if(df['enter_short'].iloc[-2] == 1):
            print('Pair: %s Entering Short at: %5f'%(pair,df['o_close'].iloc[-1]))             
            bl=bl.append({'pair':pair,'tF':timeframe,'En':df['o_close'].iloc[-1],
                          'Ex':0,'per_gain':0,'L_or_S':'short','order_status':'C','Exit':'open'},ignore_index=True)            
    
        baseTrade.liveTrade=bl
        
    def watchtrade(self,pair,df):
        # watch & check exit signal for trade
        #if exit signal found, exit the trade
        bl=baseTrade.liveTrade
        livepairs=bl['pair'].to_numpy()
        
        if pair in livepairs:
            
            #status of live pair
            idx=bl[bl['pair']==pair].index[0]
            
            #update close price for open trade
            if (bl['L_or_S'].loc[idx]=='long' and bl['Exit'].loc[idx]=='open'):
                bl['Ex'].loc[idx]=df['o_close'].iloc[-1]
                bl['per_gain'].loc[idx]=((df['o_close'].iloc[-1]-bl['En'].loc[idx])/bl['En'].loc[idx])*100
                print('watching pair',pair,'close',df['o_close'].iloc[-1])
            if (bl['L_or_S'].loc[idx]=='short' and bl['Exit'].loc[idx]=='open'):
                bl['Ex'].loc[idx]=df['o_close'].iloc[-1]
                bl['per_gain'].loc[idx]=((-df['o_close'].iloc[-1]+bl['En'].loc[idx])/bl['En'].loc[idx])*100 
                print('watching pair',pair,'close',df['o_close'].iloc[-1])
            #if exit signal (closed candle)
            #(bug: if enty forms after exit, then this logic fails
            #need to include time of candle as well)
            #then enter only with L-1 candle
            
            if(df['exit_long'].iloc[-1] == 1 and bl['Exit'].loc[idx]=='open'):
                print('Pair: %s Exiting Long at: %5f'%(pair,df['o_close'].iloc[-1]))
                bl['Ex'].loc[idx]=df['o_close'].iloc[-1]
                bl['Exit'].loc[idx]='signal'
                
            #if exit signal (closed candle)
            if(df['exit_short'].iloc[-1] == 1 and bl['Exit'].loc[idx]=='open'):
                print('Pair: %s Exiting Short at: %5f'%(pair,df['o_close'].iloc[-1]))
                bl['Ex'].loc[idx]=df['o_close'].iloc[-1]
                bl['Exit'].loc[idx]='signal'            
            
            # #check if stoploss (both long & short)
            # if(bl['L_or_S'].loc[idx]=='long' and bl['Exit'].loc[idx]=='open'):
            #     if((bl['En'].loc[idx]-df['o_close'].iloc[-1])/bl['En'].loc[idx] >=3.0):
            #         print('Pair: %s Exiting Long at: %5f'%(pair,df['o_close'].iloc[-1]))
            #         bl['Ex'].loc[idx]=df['o_close'].iloc[-1]
            #         bl['Exit'].loc[idx]='stoploss' 
                
            # if(bl['L_or_S'].loc[idx]=='short' and bl['Exit'].loc[idx]=='open'):
            #     if((-bl['En'].loc[idx]+df['o_close'].iloc[-1])/bl['En'].loc[idx] >=3.0):
            #         print('Pair: %s Exiting Short at: %5f'%(pair,df['o_close'].iloc[-1]))
            #         bl['Ex'].loc[idx]=df['o_close'].iloc[-1]
            #         bl['Exit'].loc[idx]='stoploss'               
                
        baseTrade.liveTrade=bl                
    
    def movetrade(self,pair):
        #moves completed trade from live to history
        bl=baseTrade.liveTrade
        bh=baseTrade.histTrade

        idx=bl[bl['pair']==pair].index[0]
        
        if(bl['Exit'].loc[idx] !='open'):
            bh=bh.append(bl.loc[idx])
            bl=bl.drop(idx)
            print('%s moved from live to hist'%pair)
            
        baseTrade.liveTrade=bl
        baseTrade.histTrade=bh        
