#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 14:31:22 2019
@author: Maicon Melo Alves
"""


''' Importing additional modules'''
import sys
import data
import analysis
import country_converter as cc

''' Functions '''

def prepare_data(df_top500):
    df_top500.List = df_top500.List.astype(str)
    
    #df_top500['Ranking Score'] = (500 - df_top500['Rank'] ) / (500 - 1)
    
    
    
    return df_top500

    
''' Main program '''
def main():
     
    df_top500 = data.get_data()
    
    df_top500 = prepare_data(df_top500)
    
    analysis.countries(df_top500)
    
    
    
    
    




if __name__ == "__main__":
    sys.exit(main())
