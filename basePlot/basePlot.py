#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 19:53:46 2022

@author: vino
"""
import sys
import os
from datetime import datetime
from matplotlib import pyplot as plt
import mplfinance as mpf
import matplotlib.dates as mpdates 
import numpy as np


class basePlot:
    
    def __init__(self):
        
        pass
    
class candlePlot:
   
    def __init__(self,df,plot):
        pass
        self.plot=plot
        self.getPlotCPR(df)
    
    def getPlotO(self,df):
        
        if self.plot==True:
        
            # df['En']=np.nan
            # idx=df[(df['engulf'] == 1)].index
            # if(len(idx) >0):
            #     df['En'].loc[idx]=df['o_low'].loc[idx]
            # else:
            #     df['En'].iloc[0]=df['o_low'].max()
                
            # df['ExL']=np.nan
            # idx=df[(df['exit_long'] == 1)].index
            # if(len(idx) >0):
            #     df['ExL'].loc[idx]=df['ema10'].loc[idx]
            # else:
            #     df['ExL'].iloc[0]=df['ema10'].max()  
                
            # df['EnS']=np.nan
            # idx=df[(df['enter_short'] == 1)].index
            # if(len(idx) >0):
            #     df['EnS'].loc[idx]=df['ema10'].loc[idx]
            # else:
            #     df['EnS'].iloc[0]=df['ema10'].max() 
            
            # df['ExS']=np.nan
            # idx=df[(df['exit_short'] == 1)].index
            # if(len(idx) >0):
            #     df['ExS'].loc[idx]=df['ema20'].loc[idx]
            # else:
            #     df['ExS'].iloc[0]=df['ema20'].max()
                
                
            add_plot = [ mpf.make_addplot(df['ema20'],color='orange',width=1),
                         mpf.make_addplot(df['ema50'],color='blue',width=1),
                         mpf.make_addplot(df['ema200'],color='black',width=1),
                         
                         #mpf.make_addplot(df['ema20_mstd'],color='yellow',width=1),                         
                         #mpf.make_addplot(df['ema20_pstd'],color='yellow',width=1),  
                         
                         #mpf.make_addplot(df['SL'],color='red',width=1.2,marker='_',type='scatter'),     
                         #mpf.make_addplot(df['TP'],color='green',width=1.2,marker='_',type='scatter'),
                         
                         # mpf.make_addplot(df['h1v'],color='green',marker='o',markersize=20,type='scatter'),
                         # mpf.make_addplot(df['l1v'],color='red',marker='>',markersize=18,type='scatter'),
                         # mpf.make_addplot(df['h2v'],color='blue',marker='^',markersize=16,type='scatter'),
                         # mpf.make_addplot(df['l2v'],color='orange',marker='s',markersize=14,type='scatter'),
                         
                         #mpf.make_addplot(df['eng_up'],color='green',marker='^',markersize=20,type='scatter'),    
                         #mpf.make_addplot(df['eng_down'],color='red',marker='^',markersize=20,type='scatter'),                         
                         #mpf.make_addplot(df['EnL'],color='green',width=1.2,marker='^',type='scatter'),                          
                         #mpf.make_addplot(df['EnL'],color='green',marker='^',markersize=50,type='scatter'),
                         mpf.make_addplot(df['ema20'],panel=1,color='green',marker='^',markersize=20,type='scatter'),    
                         # mpf.make_addplot(df['enter_long'],panel=1,color='green',marker='^',markersize=20,type='scatter'),       
                         # mpf.make_addplot(df['exit_long'],panel=1,color='red',marker='^',markersize=20,type='scatter'),
                         # mpf.make_addplot(df['enter_short'],panel=1,color='green',marker='<',markersize=20,type='scatter'),       
                         # mpf.make_addplot(df['exit_short'],panel=1,color='red',marker='<',markersize=20,type='scatter'),                            
                         #mpf.make_addplot(df['EnS'],panel=1,color='green',marker='v',markersize=50,type='scatter'),
                         #mpf.make_addplot(df['ExS'],panel=1,color='red',marker='v',markersize=50,type='scatter'),                                                   
                         mpf.make_addplot(df['rsi'],panel=2,color='orange',width=1.2,ylim=(10,90)),
                         mpf.make_addplot(df['rsi_ema'],panel=2,color='blue',width=1.2,ylim=(10,90)),  
                         #mpf.make_addplot(df['PSARl'],color='green',marker='o',markersize=6,type='scatter'), 
                         #mpf.make_addplot(df['PSARs'],color='red',marker='o',markersize=6,type='scatter'),                          
                         #mpf.make_addplot(df['wt1'],panel=3,color='orange',width=1.2,ylim=(-100,100)),
                         #mpf.make_addplot(df['wt2'],panel=3,color='blue',width=1.2,ylim=(-100,100)),  
                         #mpf.make_addplot(df['ema10_inc'],panel=3,color='green',width=1.2,marker='o',type='scatter'),  
                         #mpf.make_addplot(df['ema10_dec'],panel=3,color='red',width=1.2,marker='o',type='scatter'), 
                       ]
            
            tmp=df[['o_open','o_close','o_high','o_low','o_volume']]
            tmp.columns=['open','close','high','low','volume']
            
            mpf.plot(tmp,addplot=add_plot,xrotation=10,type='candle',panel_ratios=(1,0.2),figratio=(2.5,1),figscale=2.5,style='sas',\
                     savefig=dict(fname='fig.jpg',dpi=300))

        else:
            pass     
    
    def getPlotHA(self,df):
        
        #df=df.iloc[20:]
        
        if self.plot==True:
        
            df['EnL']=np.nan
            idx=df[(df['enter_long'] == 1)].index
            if(len(idx) >0):
                df['EnL'].loc[idx]=df['ema20'].loc[idx]
            else:
                df['EnL'].iloc[0]=df['ema20'].max()
                
            df['ExL']=np.nan
            idx=df[(df['exit_long'] == 1)].index
            if(len(idx) >0):
                df['ExL'].loc[idx]=df['ema10'].loc[idx]
            else:
                df['ExL'].iloc[0]=df['ema10'].max()  
                
            df['EnS']=np.nan
            idx=df[(df['enter_short'] == 1)].index
            if(len(idx) >0):
                df['EnS'].loc[idx]=df['ema10'].loc[idx]
            else:
                df['EnS'].iloc[0]=df['ema10'].max() 
            
            df['ExS']=np.nan
            idx=df[(df['exit_short'] == 1)].index
            if(len(idx) >0):
                df['ExS'].loc[idx]=df['ema20'].loc[idx]
            else:
                df['ExS'].iloc[0]=df['ema20'].max()
                
                
            add_plot = [ mpf.make_addplot(df['ema10'],panel=1,color='orange',width=1.2),
                         mpf.make_addplot(df['ema20'],panel=1,color='blue',width=1.2),
                         #mpf.make_addplot(df['EnL'],panel=1,color='green',marker='^',markersize=50,type='scatter'),
                         #mpf.make_addplot(df['ExL'],panel=1,color='red',marker='^',markersize=50,type='scatter'),                         
                         #mpf.make_addplot(df['EnS'],panel=1,color='green',marker='v',markersize=50,type='scatter'),
                         #mpf.make_addplot(df['ExS'],panel=1,color='red',marker='v',markersize=50,type='scatter'),                                                   
                         #mpf.make_addplot(df['rsi'],panel=2,color='orange',width=1.2,ylim=(10,90)),
                         #mpf.make_addplot(df['rsi_ema'],panel=2,color='blue',width=1.2,ylim=(10,90)),  
                         mpf.make_addplot(df['PSARl'],color='green',marker='o',markersize=6,type='scatter'), 
                         mpf.make_addplot(df['PSARs'],color='red',marker='o',markersize=6,type='scatter'), 
                         #mpf.make_addplot(df['wt1'],panel=3,color='orange',width=1.2,ylim=(-100,100)),
                         #mpf.make_addplot(df['wt2'],panel=3,color='blue',width=1.2,ylim=(-100,100)),  
                         #mpf.make_addplot(df['ema10_inc'],panel=3,color='green',width=1.2,marker='o',type='scatter'),  
                         #mpf.make_addplot(df['ema10_dec'],panel=3,color='red',width=1.2,marker='o',type='scatter'), 
                       ]

            mpf.plot(df,addplot=add_plot,xrotation=10,type='candle',panel_ratios=(1,0.2),figratio=(1,2),figscale=2,style='sas')

        else:
            pass        

    def getPlotCPR(self,df):
        
        df=df.iloc[:3000]
        
        df['enter_long1']=df['enter_long'].copy()
        df['exit_long1']=df['exit_long'].copy()
        df['enter_short1']=df['enter_short'].copy()
        df['exit_short1']=df['exit_short'].copy()
        
        for i in range(df.shape[0]):
            if(df['enter_long'].iloc[i]==1):
                df['enter_long1'].iloc[i]=df['low'].iloc[i]
            else:
                df['enter_long1'].iloc[i]=np.nan
                
            if(df['exit_long'].iloc[i]==1):
                df['exit_long1'].iloc[i]=df['low'].iloc[i]                
            else:
                df['exit_long1'].iloc[i]=np.nan
                
            # if(df['enter_short'].iloc[i]==1):
            #     df['enter_short1'].iloc[i]=df['high'].iloc[i]
            # else:
            #     df['enter_short1'].iloc[i]=np.nan
                
            # if(df['exit_short'].iloc[i]==1):
            #     df['exit_short1'].iloc[i]=df['high'].iloc[i]                
            # else:
            #     df['exit_short1'].iloc[i]=np.nan                
                
        if self.plot==True:
                       
            ms=0.1   
            lw=0.1
            
            add_plot = [ mpf.make_addplot(df['ema20'],color='orange',width=lw),
                         mpf.make_addplot(df['ema50'],color='blue',width=lw),
                         mpf.make_addplot(df['pivot'],color='blue',type='scatter',markersize=ms,marker='o'),
                         mpf.make_addplot(df['BC'],color='blue',type='scatter',markersize=ms,marker='o'),                         
                         mpf.make_addplot(df['TC'],color='blue',type='scatter',markersize=ms,marker='o'), 
                         mpf.make_addplot(df['S1'],color='red',type='scatter',markersize=ms,marker='o'),   
                         mpf.make_addplot(df['S2'],color='red',type='scatter',markersize=ms,marker='o'),   
                         mpf.make_addplot(df['R1'],color='green',type='scatter',markersize=ms,marker='o'),   
                         mpf.make_addplot(df['R2'],color='green',type='scatter',markersize=ms,marker='o'),
                         mpf.make_addplot(df['enter_long'],color='green',type='scatter',markersize=5,marker='^'),
                         mpf.make_addplot(df['exit_long'],color='red',type='scatter',markersize=5,marker='^'),
                         #mpf.make_addplot(df['enter_short'],color='green',type='scatter',markersize=5,marker='o'),
                         #mpf.make_addplot(df['exit_short'],color='red',type='scatter',markersize=5,marker='o'),
                         mpf.make_addplot(df['enter_long1'],color='green',type='scatter',markersize=5,marker='^'),    
                         mpf.make_addplot(df['exit_long1'],color='red',type='scatter',markersize=5,marker='^'), 
                         #mpf.make_addplot(df['enter_short1'],color='green',type='scatter',markersize=5,marker='v'),    
                         #mpf.make_addplot(df['exit_short1'],color='red',type='scatter',markersize=5,marker='v'),                           
                       ]

            tmp=df[['open','close','high','low','volume']]
            tmp.columns=['open','close','high','low','volume']
            
            mpf.plot(tmp,addplot=add_plot,xrotation=10,type='candle',figratio=(5,1),figscale=2,style='sas',\
                                 savefig=dict(fname='fig.jpg',dpi=300))
        else:
            pass         
        
    @staticmethod    
    def plotShaprpe(tmp): 
        
        tmp['cum_pnl']=0
        for i in range(len(tmp)):
            tmp['cum_pnl'].iloc[i]=tmp['per_gain'].iloc[:i+1].sum()
                
        plt.figure()
        plt.plot(tmp.index,tmp['cum_pnl'])
        plt.xlabel('No of Trade')
        plt.ylabel('Cum. % profit')
        plt.show()