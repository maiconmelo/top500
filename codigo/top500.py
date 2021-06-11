#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 14:31:22 2019
@author: Maicon Melo Alves
"""


''' Importing additional modules'''
import sys
import requests
import wget
import itertools 
import os
import pandas as pd
from lxml import html
from openpyxl import load_workbook


''' Constants '''
first_year = 1993
last_year = 2020
years_range = range(first_year, last_year + 1)
#years_range = range(2007, 2009)
release_months = ["06", "11"]
login_url = "https://www.top500.org/accounts/login/"
my_username =  "maiconmeloalves"
my_password = "jKVDvrmyM9zERXd"
data_filename = "top500.csv"

''' Functions '''

def login_website(username, password, login_url):
    session = requests.session()
    result = session.get(login_url)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
    
    payload = {
            "login": username, 
            "password": password, 
            "csrfmiddlewaretoken": authenticity_token
    }

    session.post(login_url, data = payload, headers = dict(referer=login_url))
    
    return session
    

def process_columns(raw_data):
    for i, row in raw_data.iterrows():
        if row.notnull().all():
            data = raw_data.iloc[(i+1):].reset_index(drop=True)
            data.columns = list(raw_data.iloc[i])
            break
    
    return data
    
          
def download_data(session):
    released_dates = itertools.product(years_range, release_months)

    df_top500 = pd.DataFrame()

    for year, month in released_dates:
        list_url_xls = f"https://www.top500.org/lists/top500/{year}/{month}/download/TOP500_{year}{month}.xls"
        list_url_xlsx = f"https://www.top500.org/lists/top500/{year}/{month}/download/TOP500_{year}{month}.xlsx"
        
        result = session.get(list_url_xls, stream=True)
        if result.status_code != 200:
            result = session.get(list_url_xlsx, stream=True)
        
        raw_data = pd.read_excel(result.content, header=None)
        df_list = process_columns(raw_data)
        df_list['List'] = f"{year}.{month}"
        df_top500 = df_top500.append(df_list, ignore_index=True)
        print(f"Sucessfuly downloaded list {year}.{month}")

    return df_top500

def get_data():
    print("Getting data...")
    if os.path.isfile(data_filename):
        df_top500 = pd.read_csv(data_filename)
    else:
        print("Data not found. Downloading...")
        session = login_website(my_username, my_password, login_url)
        df_top500 = download_data(session)
        df_top500.to_csv(data_filename)
    
    print("Done!")

    return df_top500
    

def pre_processing_data(df_top500):
    pass


  

    
''' Main program '''
def main():
     
    df_top500 = get_data()
    
    df_top500 = pre_processing_data(df_top500)
    
    
    
    
    




if __name__ == "__main__":
    sys.exit(main())
