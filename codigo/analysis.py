#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 10:46:31 2021

@author: maicon
"""


import country_converter as cc
import plot 
import pandas as pd



def countries_summary(df_top500):
    df = df_top500.groupby('List')['Country'].value_counts()
    df = df.reset_index(name="Occurrences")
    ds = df.groupby('Country').median() > 1
    ds = ds[ds['Occurrences'] == False]
    for country in ds.index:
        df = df[df['Country'] != country]
        
   
    fig = plot.boxplot(df, 'Country', 'Occurrences')
    
    fig.write_image("figuras/countries_summary.svg")
    fig.write_html("html/countries_summary.html")


def countries_evolution(df_top500):
    df = df_top500.groupby('List')['Country'].value_counts()
    df = df.reset_index(name="Occurrences")
    ds = df.groupby('Country').std() > 30
    ds = ds[ds['Occurrences'] == False]
    for country in ds.index:
        df = df[df['Country'] != country]
   
    fig = plot.line(df, 'List', 'Occurrences', 'Country')
    
    fig.write_image("figuras/countries_evolution.svg")
    fig.write_html("html/countries_evolution.html")

def countries_presence_top5(df_top500):
    ds = df_top500[df_top500['Rank'] <= 5]['Country'].value_counts()
    df = pd.DataFrame({'Country':ds.index, 'Occurrences':ds.values})
    
    fig = plot.bar(df[0:10], "Occurrences", "Country")
    fig.write_image("figuras/ocorrencias_por_pais_barra_top5.svg")


def countries_historic_presence(df_top500):
    ds = df_top500['Country'].value_counts()
    df = pd.DataFrame({'Country':ds.index, 'Occurrences':ds.values})
    df['Code'] = cc.convert(df['Country'], to="ISO3")
    fig = plot.geo_map(df['Code'], 
                       df['Occurrences'], 
                       df.index, 
                       'TOP500 - Ocorrências por país', 
                       'Ocorrências' 
    )
    fig.write_html("html/ocorrencias_por_pais_mapa.html")
    fig.write_image("figuras/ocorrencias_por_pais_mapa.svg")
    
    fig = plot.bar(df[0:10], "Occurrences", "Country")
    fig.write_image("figuras/ocorrencias_por_pais_barra.svg")


def countries_nowadays_presence(df_top500):
    df_last_list = df_top500[df_top500['List'] == "2020.11"]
    ds = df_last_list['Country'].value_counts()
    df = pd.DataFrame({'Country':ds.index, 'Occurrences':ds.values})
    df['Code'] = cc.convert(df['Country'], to="ISO3")
    fig = plot.geo_map(df['Code'], 
                       df['Occurrences'], 
                       df.index, 
                       'TOP500 - Ocorrências por país', 
                       'Ocorrências' 
    )
    fig.write_html("html/ocorrencias_ultima_lista_por_pais_mapa.html")
    fig.write_image("figuras/ocorrencias_ultima_lista_por_pais_mapa.svg")
    
    fig = plot.bar(df[0:10], "Occurrences", "Country")
    fig.write_image("figuras/ocorrencias_ultima_lista_por_pais_barra.svg")


    

def countries(df_top500):
    countries_evolution(df_top500)
    countries_historic_presence(df_top500)
    countries_nowadays_presence(df_top500)
    countries_presence_top5(df_top500)
    countries_summary(df_top500)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    