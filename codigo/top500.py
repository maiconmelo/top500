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
import prediction
import country_converter as cc

''' Functions '''

   
''' Main program '''
def main():
     
    df_top500 = data.get_data()
    
    #analysis.countries(df_top500)
    #analysis.efficiency(df_top500)
    prediction.exaflop(df_top500)
    
    
    
    
    




if __name__ == "__main__":
    sys.exit(main())
