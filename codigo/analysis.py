#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 10:46:31 2021

@author: maicon
"""


import country_converter as cc
import plot 
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import export_graphviz 
import statsmodels.api as sm
from statsmodels.formula.api import ols
import scipy.stats as stats




def countries_summary(df_top500):
    df = df_top500.groupby('List')['Country'].value_counts()
    df = df.reset_index(name="Occurrences")
    ds = df.groupby('Country').median() > 1
    ds = ds[ds['Occurrences'] == False]
    for country in ds.index:
        df = df[df['Country'] != country]
        
   
    labels = {"Country": "Países", "Occurrences":"Ocorrências"}
    fig = plot.boxplot(df, 'Country', 'Occurrences', labels, "Ocorrências no Top500", [0,500])
    
    fig.write_image("figuras/countries_summary.svg")
    fig.write_html("html/countries_summary.html")


def individual_evolution(df_top500, country):
    df = df_top500.groupby('List')['Country'].value_counts()
    df = df.reset_index(name="Occurrences")
    df = df[df['Country'] == country]
    
    labels = {"Country": "Países", "Occurrences":"Ocorrências", 'List':'Lista publicada'}   
    fig = plot.line(df, 'List', 'Occurrences', 'Country', labels, "Participação dos países no Top500" )
    
    
    fig.write_image(f"figuras/{country}_evolution.svg")
    fig.write_html(f"html/{country}_evolution.html")


def countries_evolution(df_top500):
    df = df_top500.groupby('List')['Country'].value_counts()
    df = df.reset_index(name="Occurrences")
    ds = df.groupby('Country').std() > 10
    ds = ds[ds['Occurrences'] == False]
    for country in ds.index:
        df = df[df['Country'] != country]
   
    
    labels = {"Country": "Países", "Occurrences":"Ocorrências", 'List':'Lista publicada'}   
    fig = plot.line(df, 'List', 'Occurrences', 'Country', labels, "Participação dos países no Top500" )
    
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
                       'Total ocorrências no TOP500 por país', 
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
    df = df_top500.copy()
    df.List = df.List.astype(str)

    
    countries_evolution(df)
    countries_historic_presence(df)
    countries_nowadays_presence(df)
    countries_presence_top5(df)
    countries_summary(df)
    individual_evolution(df, 'Brazil')
    
    
def anova_table(aov):
    aov['mean_sq'] = aov[:]['sum_sq']/aov[:]['df']

    aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])

    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*aov['mean_sq'][-1]))/(sum(aov['sum_sq'])+aov['mean_sq'][-1])

    cols = ['sum_sq', 'df', 'mean_sq', 'F', 'PR(>F)', 'eta_sq', 'omega_sq']
    aov = aov[cols]
    



    
def eff(df_top500):
    df = df_top500.drop(df_top500[df_top500['Efficiency'] < 1].index)
    df = df[df['List'] >= 2020]
    df = df[['Processor Technology', 
            'Operating System',
            'Interconnect Family',
            'Accelerator',
            'Efficiency']]
    
    df = df.rename({'Processor Technology': 'processor_technology', 
                    'Operating System': 'operating_system',
                    'Interconnect Family': 'interconnect_family', 
                    'Accelerator': 'accelerator', 
                    'Efficiency': 'efficiency'},
                    axis='columns')
    
    
    
    labels = {"Processor Technology": "Países", "Efficiency":"Ocorrências"}
    fig = plot.boxplot(df, 'processor_technology', 'efficiency', labels, "Ocorrências no Top500", [0,100])
    fig.write_image("figuras/efficiency.svg")
    fig.write_html("html/efficiency.html") 
    
    

    model = ols('efficiency ~ C(processor_technology)', data=df).fit()
    aov_table = sm.stats.anova_lm(model, typ=2)
    anova_table(aov_table)
    print(stats.shapiro(model.resid))
    print(aov_table['PR(>F)'][0])
    
    model = ols('efficiency ~ C(operating_system)', data=df).fit()
    aov_table = sm.stats.anova_lm(model, typ=2)
    anova_table(aov_table)
    print(stats.shapiro(model.resid))
    print(aov_table['PR(>F)'][0])
    
    model = ols('efficiency ~ C(interconnect_family)', data=df).fit()
    aov_table = sm.stats.anova_lm(model, typ=2)
    anova_table(aov_table)
    print(stats.shapiro(model.resid))
    print(aov_table['PR(>F)'][0])
    
    model = ols('efficiency ~ C(accelerator)', data=df).fit()
    aov_table = sm.stats.anova_lm(model, typ=2)
    anova_table(aov_table)
    print(stats.shapiro(model.resid))
    print(aov_table['PR(>F)'][0])
    
    

    
def efficiency(df_top500):
    eff(df_top500)
    
    
    
    
    
    
    
    
    
    
    
    
    
    