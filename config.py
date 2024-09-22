#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 19:53:46 2022

@author: vino
"""
import sys
import os
 
def kcf_pairs_stable8():

    pairs=["BTC/USDT:USDT",
        "ETH/USDT:USDT",
        "APE/USDT:USDT",
        "LUNC/USDT:USDT",
        "GALA/USDT:USDT",
        "KDA/USDT:USDT",
        "JASMY/USDT:USDT",
        ]
    
    return pairs

def kcf_pairs_SR():

    pairs=["BTC/USDT:USDT",
        "ETH/USDT:USDT",
        "LUNC/USDT:USDT",
        "GALA/USDT:USDT",
        "KDA/USDT:USDT",
        "JASMY/USDT:USDT",
        "ADA/USDT:USDT",
        "OP/USDT:USDT",
        "DYDX/USDT:USDT",
	"AAVE/USDT:USDT",
	"ALGO/USDT:USDT",
	"AVAX/USDT:USDT",
	"APT/USDT:USDT",
	"APE/USDT:USDT"
        ]

    return pairs
           
def kcf_pairs_stable100():

    pairs=["BTC/USDT:USDT",
        "ETH/USDT:USDT",
        "BCH/USDT:USDT",
        "LINK/USDT:USDT",
        "UNI/USDT:USDT",
        "YFI/USDT:USDT",
        "EOS/USDT:USDT",
        "DOT/USDT:USDT",
        "FIL/USDT:USDT",
        "ADA/USDT:USDT",
        "XRP/USDT:USDT",
        "LTC/USDT:USDT",
        "TRX/USDT:USDT",
        "GRT/USDT:USDT",
        "XLM/USDT:USDT",
        "1INCH/USDT:USDT",
        "DASH/USDT:USDT",
        "AAVE/USDT:USDT",
        "KSM/USDT:USDT",
        "DOGE/USDT:USDT",
        "VET/USDT:USDT",
        "BNB/USDT:USDT",
        "SOL/USDT:USDT",
        "CRV/USDT:USDT",
        "ALGO/USDT:USDT",
        "AVAX/USDT:USDT",
        "FTM/USDT:USDT",
        "THETA/USDT:USDT",
        "ATOM/USDT:USDT",
        "CHZ/USDT:USDT",
        "ENJ/USDT:USDT",
        "MANA/USDT:USDT",
        "BAT/USDT:USDT",
        "QTUM/USDT:USDT",
        "ONT/USDT:USDT",
        "XMR/USDT:USDT",
        "ETC/USDT:USDT",
        "BAND/USDT:USDT",
        "MKR/USDT:USDT",
        "RVN/USDT:USDT",
        "SHIB/USDT:USDT",
        "ICP/USDT:USDT",
        "DYDX/USDT:USDT",
        "AXS/USDT:USDT",
        "HBAR/USDT:USDT",
        "EGLD/USDT:USDT",
        "NEAR/USDT:USDT",
        "SAND/USDT:USDT",
        "C98/USDT:USDT",
        "ONE/USDT:USDT",
        "VRA/USDT:USDT",
        "GALA/USDT:USDT",
        "TLM/USDT:USDT",
        "CHR/USDT:USDT",
        "LRC/USDT:USDT",
        "FLOW/USDT:USDT",
        "RNDR/USDT:USDT",
        "IOTX/USDT:USDT",
        "CRO/USDT:USDT",
        "PEOPLE/USDT:USDT",
        "OMG/USDT:USDT",
        "LINA/USDT:USDT",
        "IMX/USDT:USDT",
        "CELR/USDT:USDT",
        "ENS/USDT:USDT",
        "CELO/USDT:USDT",
        "KNC/USDT:USDT",
        "SOS/USDT:USDT",
        "ROSE/USDT:USDT",
        "AGLD/USDT:USDT",
        "APE/USDT:USDT",
        "JASMY/USDT:USDT",
        "ZIL/USDT:USDT",
        "GMT/USDT:USDT",
        "RUNE/USDT:USDT",
        "AUDIO/USDT:USDT",
        "KDA/USDT:USDT",
        "KAVA/USDT:USDT",
        "BAL/USDT:USDT",
        "GAL/USDT:USDT",
        "LUNA/USDT:USDT",
        "LUNC/USDT:USDT",
        "OP/USDT:USDT",
        "UNFI/USDT:USDT",
        "DUSK/USDT:USDT",
        "STORJ/USDT:USDT",
        "ANC/USDT:USDT",
        "RSR/USDT:USDT",
        "OGN/USDT:USDT",
        "TRB/USDT:USDT",
        "INJ/USDT:USDT"]
    
    return pairs           

def spot_pairs():
    pairs=["FLUX/USDT"]       
