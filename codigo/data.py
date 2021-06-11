#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 09:26:28 2021

@author: maicon
"""

import requests
import itertools 
import os
import config as cfg
import pandas as pd
from lxml import html

def login_website():
    session = requests.session()
    result = session.get(cfg.login_url)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
    
    payload = {
            "login": cfg.username, 
            "password": cfg.password, 
            "csrfmiddlewaretoken": authenticity_token
    }

    session.post(cfg.login_url, data = payload, headers = dict(referer=cfg.login_url))
    
    return session
    

def process_columns(raw_data):
    for i, row in raw_data.iterrows():
        if row.notnull().all():
            data = raw_data.iloc[(i+1):].reset_index(drop=True)
            data.columns = list(raw_data.iloc[i])
            break
    
    return data
    
          
def download_data(session):
    released_dates = itertools.product(cfg.years_range, cfg.release_months)

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
        df_top500 = df_top500.append(df_list, ignore_index=False)
        print(f"Sucessfuly downloaded list {year}.{month}")

    return df_top500

def get_data():
    print("Getting data...")
    if os.path.isfile(cfg.data_filename):
        df_top500 = pd.read_csv(cfg.data_filename)
    else:
        print("Data not found.")
        print("Downloading...")
        session = login_website()
        df_top500 = download_data(session)
        df_top500.to_csv(cfg.data_filename)
    
    print("Done!")

    return df_top500