#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 10:46:31 2021

@author: maicon
"""


import plot 
import config
import pandas as pd
import country_converter as cc
import statsmodels.api as sm
import scipy.stats as stats
from statsmodels.formula.api import ols





def countries_summary(df):
    df = df.groupby('list').country.value_counts()
    df = df.reset_index(name="occurrences")
    ds = df.groupby('country').median() > 1
    ds = ds[ds.occurrences == False]
    for country in ds.index:
        df = df[df.country != country]
        
   
    labels = {"country": "Países", "occurrences":"Ocorrências"}
    fig = plot.boxplot(df, 'country', 'occurrences', labels, "Ocorrências no Top500", [0,500])
    plot.save(fig, "countries_summary") 
    
   

def individual_evolution(df, country):
    df = df.groupby('list').country.value_counts()
    df = df.reset_index(name="occurrences")
    df = df[df.country == country]
    
    labels = {"country": "Países", "occurrences":"Ocorrências", 'list':'Lista publicada'}   
    fig = plot.line(df, 'list', 'occurrences', 'country', labels, "Participação dos países no Top500" )
    plot.save(fig, f"{country}_evolution") 
    

def countries_evolution(df):
    df = df.groupby('list').country.value_counts()
    df = df.reset_index(name="occurrences")
    ds = df.groupby('country').std() > 10
    ds = ds[ds.occurrences == False]
    for country in ds.index:
        df = df[df.country != country]
   
    
    labels = {"country": "Países", "occurrences":"Ocorrências", 'list':'Lista publicada'}   
    fig = plot.line(df, 'list', 'occurrences', 'country', labels, "Participação dos países no Top500" )
    plot.save(fig, "countries_evolution")    



def countries_historic_presence(df):
    ds = df.country.value_counts()
    df = pd.DataFrame({'country':ds.index, 'occurrences':ds.values})
    df['code'] = cc.convert(df.country, to="ISO3")
    fig = plot.geo_map(df.code, 
                       df.occurrences, 
                       df.index, 
                       'Total ocorrências no TOP500 por país', 
                       'Ocorrências' 
    )
    plot.save(fig, "mapa_ocorrencias")    



def countries(df_top500):
    df = df_top500.copy()
    df.list = df.list.astype(str)

    countries_evolution(df)
    countries_historic_presence(df)
    countries_summary(df)
    individual_evolution(df, 'Brazil')
    
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
    #fig.write_image("figuras/efficiency.svg")
    fig.write_html("html/efficiency_processortech.html") 
    
    fig = plot.boxplot(df, 'operating_system', 'efficiency', labels, "Ocorrências no Top500", [0,100])
    #fig.write_image("figuras/efficiency.svg")
    fig.write_html("html/efficiency_operatingsystem.html") 
    
    fig = plot.boxplot(df, 'interconnect_family', 'efficiency', labels, "Ocorrências no Top500", [0,100])
    #fig.write_image("figuras/efficiency.svg")
    fig.write_html("html/efficiency_interconnectfamily.html") 
    
    fig = plot.boxplot(df, 'accelerator', 'efficiency', labels, "Ocorrências no Top500", [0,100])
    #fig.write_image("figuras/efficiency.svg")
    fig.write_html("html/efficiency_accelerator.html") 


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
    
    
    
    
    
    
    
    
    
    
    
    
    
    