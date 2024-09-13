#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 19:53:46 2022

@author: vino
"""
import sys
import ccxt
sys.path.append('/home/vino/trade_analysis/api_key')
from api_key import KCF_API_KEY,KCF_API_SECRET

class baseExchange:
    '''
    class: baseExchange
    This class definition loads the required exchange to pull the market data
    '''
    def __init__(self):
        
        print('Loading Exchange Details')
        
    def getExchange(self):
        '''
        This method connects with the exchange

        Returns
        -------
        exchange : TYPE
            DESCRIPTION.

        '''
        try:
            exchange = ccxt.kucoinfutures({
                'enableRateLimit': True,
                'adjustForTimeDifference': True,
                "apiKey": KCF_API_KEY,
                "secret": KCF_API_SECRET
            })
        
        except:
            raise Exception("Load exchange failed")
        print('Exchange Loaded sucessfully.!!!')
        return exchange
    
    def getSpotExchange(self):
        '''
        This method connects with the exchange

        Returns
        -------
        exchange : TYPE
            DESCRIPTION.

        '''
        try:
            exchange = ccxt.kucoin({
                'enableRateLimit': True,
                'adjustForTimeDifference': True,
                "apiKey": KCF_API_KEY,
                "secret": KCF_API_SECRET
            })
        
        except:
            raise Exception("Load exchange failed")
        print('Exchange Loaded sucessfully.!!!')
        return exchange
