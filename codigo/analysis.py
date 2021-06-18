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





def countries_summary(df_analysis):
    df = df_analysis.groupby('list').country.value_counts()
    df = df.reset_index(name="occurrences")
    ds = df.groupby('country').median() > 1
    ds = ds[ds.occurrences == False]
    for country in ds.index:
        df = df[df.country != country]
        
   
    labels = {"country": "Países", "occurrences":"Ocorrências"}
    fig = plot.boxplot(df, 
                       'country', 
                       'occurrences', 
                       labels, 
                       "Ocorrências no Top500", 
                       [0,500], 
                       False
    )
    plot.save(fig, "paises_resumo") 
    
   

def individual_evolution(df_analysis, country):
    df = df_analysis.groupby('list').country.value_counts()
    df = df.reset_index(name="occurrences")
    df = df[df.country == country]
    
    labels = {"country": "Países", "occurrences":"Ocorrências", 'list':'Lista publicada'}   
    fig = plot.line(df, 
                    'list', 
                    'occurrences', 
                    'country', 
                    labels, 
                    "Evolução da participação no Top500", 
                    [0,100]
    )
    plot.save(fig, f"{country}_evolucao") 
    

def countries_evolution(df_analysis):
    df = df_analysis.groupby('list').country.value_counts()
    df = df.reset_index(name="occurrences")
    ds = df.groupby('country').std() > 20
    ds = ds[ds.occurrences == False]
    for country in ds.index:
        df = df[df.country != country]
   
    
    labels = {"country": "Países", "occurrences":"Ocorrências", 'list':'Lista publicada'}   
    fig = plot.line(df, 
                    'list', 
                    'occurrences', 
                    'country', 
                    labels, 
                    "Evolução da participação no Top500", 
                    [0,500]
    )
    plot.save(fig, "paises_evolucao")    



def countries_historic_presence(df_analysis):
    ds = df_analysis.country.value_counts()
    df = pd.DataFrame({'country':ds.index, 'occurrences':ds.values})
    df['code'] = cc.convert(df.country, to="ISO3")
    fig = plot.geo_map(df.code, 
                       df.occurrences, 
                       df.index, 
                       'Total ocorrências no TOP500 por país', 
                       'Ocorrências' 
    )
    plot.save(fig, "mapa_ocorrencias")    



    
def interconnect(df_analysis):
    df = df_analysis.drop(df_analysis[df_analysis.efficiency > 100].index)
    df = df.drop(df[df.efficiency <= 0].index)
    df = df[df.list >= 2020]
    
    labels = {"interconnect_family": "Tecnologia de Interconexão",
              "efficiency":"Eficiência (%)"
    }
   
    fig = plot.boxplot(df, 
                       'interconnect_family', 
                       'efficiency', 
                       labels, 
                       "Eficiência por Tecnologia de Interconexão (Listas 2020.06 e 2020.11)",
                       [0,100],
                       False

    )
    plot.save(fig, "eficiencia_interconexao")    

def processor(df_analysis):
    df = df_analysis.drop(df_analysis[df_analysis.efficiency > 100].index)
    df = df.drop(df[df.efficiency <= 0].index)
    df = df[df.list >= 2020]
    
   
    
    labels = {"processor_technology": "Tecnologia do Processador",
              "efficiency":"Eficiência (%)"
    }
   
    fig = plot.boxplot(df, 
                       'processor_technology', 
                       'efficiency', 
                       labels, 
                       "Eficiência por Tecnologia do Processador (Listas 2020.06 e 2020.11)",
                       [0,100],
                       False
    )
    plot.save(fig, "eficiencia_processador")    



def historic_rmax(df_analysis):
    #df = df_analysis.drop(df_analysis[df_analysis.efficiency > 100].index)
    #df = df.drop(df[df.efficiency <= 0].index)
    df = df_analysis[df_analysis['rank'] == 1]
    df.list = df.list.astype(str)
    
    labels = {"list": "Listas", "rmax":"Desempenho (TFlops)"}   
    fig = plot.line(df, 
                    'list', 
                    'rmax', 
                    None, 
                    labels, 
                    "Desempenho Máximo dos Supercomputadores no Top500", 
                    [0,500000]
    )
    plot.save(fig, "desempenho_historico") 


def historic(df_analysis):
    df = df_analysis.drop(df_analysis[df_analysis.efficiency > 100].index)
    df = df.drop(df[df.efficiency <= 0].index)
    df.list = df.list.astype(str)
    df = df.groupby('list').efficiency.mean()
    df = df.reset_index(name="efficiency")
    
    labels = {"list": "Listas", "efficiency":"Eficiência média (%)"}   
    fig = plot.line(df, 
                    'list', 
                    'efficiency', 
                    None, 
                    labels, 
                    "Eficiência Média dos Supercomputadores no Top500", 
                    [0,100]
    )
    plot.save(fig, "eficiencia_historico") 


def variability(df_analysis):
    df = df_analysis.drop(df_analysis[df_analysis.efficiency > 100].index)
    df = df.drop(df[df.efficiency <= 0].index)
    df = df[df.list >= 2020]
    
    df.list = df.list.astype(str)
    labels = {"list": "Listas", "efficiency":"Eficiência (%)"}   
    fig = plot.boxplot(df, 
                       'list', 
                       'efficiency', 
                       labels, 
                       "Eficiência dos Supercomputadores no Top500",
                       [0,100],
                       "all"
    )
    plot.save(fig, "eficiencia_variacao") 
    
    
def efficiency(df_top500):  
    df_analysis = df_top500.copy()
    
    historic(df_analysis)
    historic_rmax(df_analysis)
    variability(df_analysis)
    interconnect(df_analysis)
    processor(df_analysis)
    
def countries(df_top500):
    df_analysis = df_top500.copy()
    df_analysis.list = df_analysis.list.astype(str)

    countries_evolution(df_analysis)
    countries_historic_presence(df_analysis)
    countries_summary(df_analysis)
    individual_evolution(df_analysis, 'Denmark')
    
    
    
    
    
    
    
    
    
    
    
    
    
    