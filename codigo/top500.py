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


''' Functions '''

   

def pre_processing_data(df_top500):
    pass

 

    
''' Main program '''
def main():
     
    df_top500 = data.get_data()
    
    df_top500 = pre_processing_data(df_top500)
    
    analysis.countries_ocurrences(df_top500)
    
    
    




if __name__ == "__main__":
    sys.exit(main())
