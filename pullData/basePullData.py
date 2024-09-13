#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 19:53:46 2022

@author: vino
"""
import sys
import os

import ccxt 
import pandas_ta as ta
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
import mplfinance as mpf
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpdates 
import numpy as np
import warnings
from termcolor import colored
import math
warnings.simplefilter(action='ignore') 

class basePullData:
    '''
    class: basePullData
    
    This is a base class that pulls data from the exchage. The actual and higher time frame data is pulled. 
    Both candle & HA candle data is availabe.
    '''
    
    def __init__(self,exchange,pair,timeframe='1h',htimeframe='4h',limit=100,plot=False):
        '''
        Parameters
        ----------
        exchange : TYPE
            DESCRIPTION.
        pair : TYPE
            DESCRIPTION.
        timeframe : TYPE, optional
            DESCRIPTION. The default is '1h'.
        htimeframe : TYPE, optional
            DESCRIPTION. The default is '4h'.
        limit : TYPE, optional
            DESCRIPTION. The default is 100.
        plot : TYPE, optional
            DESCRIPTION. The default is False.
        
        df_h : higher time frame data
        df   : actual timeframe data
        In df columns, o_open indicates original bar open & open indicates HA bar open. 

        Returns
        -------
        None.
        '''
        
        self.exhange=exchange
        self.pair=pair
        self.timeframe=timeframe
        self.limit=limit
        self.htimeframe=htimeframe
        
        #print('Pulling data %s-%s'%(self.pair,self.htimeframe))
        # #higher timeframe
        # self.df_h=self.get_bars(self.exhange,self.pair,self.htimeframe,self.limit)
        # df_h_ha=self.get_heikin_ashi(self.df_h)
        # self.df_h = self.df_h.join(df_h_ha)
        
        #actual timeframe
        #print('Pulling data %s-%s'%(self.pair,self.timeframe))
        self.df=self.get_bars(self.exhange,self.pair,self.timeframe,self.limit)
        df_ha=self.get_heikin_ashi(self.df)
        self.df = self.df.join(df_ha)
        
        #assign same time fraem for hr time frame
        self.df_h=self.df
        
        cols=['open','close','high','low']
        self.df[cols] = self.df[cols].apply(pd.to_numeric)
        
        
    def get_bars(self,exchange,pair,timeframe,limit=100):
        '''
        Pulls the candle data from exchange

        Parameters
        ----------
        exchange : TYPE
            DESCRIPTION.
        pair : TYPE
            DESCRIPTION.
        timeframe : TYPE
            DESCRIPTION.
        limit : TYPE, optional
            DESCRIPTION. The default is 100.

        Returns
        -------
        df_tmp : TYPE
            DESCRIPTION.

        '''
        tmp_bar=pd.DataFrame([],columns=['time','o_open','o_high','o_low','o_close','o_volume'])
        if(limit == 2000):
            tmp=[2000,1800,1600,1400,1200,1000,800,600,400,200]
            for i in range(len(tmp)):
                tmp_bar1=exchange.fetch_ohlcv(pair,timeframe=timeframe,limit=tmp[i])
                tmp_bar2=pd.DataFrame(tmp_bar1,columns=['time','o_open','o_high','o_low','o_close','o_volume'])
                tmp_bar=tmp_bar.append(tmp_bar2,ignore_index=True)
             
            df_tmp=tmp_bar.drop_duplicates(subset=['time'])
            
            df_tmp['time']=pd.to_datetime(df_tmp['time'],unit='ms')
        
            df_tmp=df_tmp.set_index('time')     
            
        if(limit == 600):
            tmp=[600,400,200]
            for i in range(len(tmp)):
                tmp_bar1=exchange.fetch_ohlcv(pair,timeframe=timeframe,limit=tmp[i])
                tmp_bar2=pd.DataFrame(tmp_bar1,columns=['time','o_open','o_high','o_low','o_close','o_volume'])
                tmp_bar=tmp_bar.append(tmp_bar2,ignore_index=True)
             
            df_tmp=tmp_bar.drop_duplicates(subset=['time'])
            
            df_tmp['time']=pd.to_datetime(df_tmp['time'],unit='ms')
        
            df_tmp=df_tmp.set_index('time')                 
        
        else:
        
            bars=exchange.fetch_ohlcv(pair,timeframe=timeframe,limit=limit)
        
            df_tmp=pd.DataFrame(bars,columns=['time','o_open','o_high','o_low','o_close','o_volume'])
            
            df_tmp['o_time']=df_tmp['time'].copy()
            df_tmp['time']=pd.to_datetime(df_tmp['time'],unit='ms')
            
        
            df_tmp=df_tmp.set_index('time')
            
            
        #df_tmp=df_tmp.iloc[:-50]
        return df_tmp


    def get_heikin_ashi(self,df):
        '''
        converts candle data into HA candle data 

        Parameters
        ----------
        df : TYPE
            DESCRIPTION.

        Returns
        -------
        heikin_ashi_df : TYPE
            DESCRIPTION.

        '''
        
        heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['open', 'high', 'low', 'close'])
        
        heikin_ashi_df['close'] = (df['o_open'] + df['o_high'] + df['o_low'] + df['o_close']) / 4
        
        for i in range(len(df)):
            if i == 0:
                heikin_ashi_df.iat[0, 0] = df['o_open'].iloc[0]
            else:
                heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2
            
        heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['o_high']).max(axis=1)

        heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['o_low']).min(axis=1)
        
        heikin_ashi_df['volume'] = df['o_volume'] 
        
        return heikin_ashi_df
    
    def checkCandleTime(self):
        '''
        This method checks the time of the candle to make sure the latest candle is pulled.
        If not latest candle, raise a warning.
        Returns
        -------
        None.

        '''
        pass