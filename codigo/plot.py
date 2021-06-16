#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 14:41:17 2021

@author: maicon
"""

import plotly.graph_objects as go
import plotly.express as px


def line(data, x, y, color, labels, title):
    
    fig = px.line(data, x=x, y=y, title=title, labels=labels, color=color, height=600, width=800)
    fig.update_yaxes(range=[0,100])
    return fig

def boxplot(data, x, y, labels, title):
    fig = px.box(data, x=x, y=y, title=title, points=False, labels=labels, height=600, width=800)
    
    return fig

def bar(data, x, y):
    fig = px.bar(data, x=x, y=y, orientation='h')
    
    return fig


def geo_map(positions, data, label, title, legend):
    fig = go.Figure(data=go.Choropleth(
        locations = positions,
        z = data,
        text = label,
        colorscale = 'Blues',
        autocolorscale=True,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title = legend
    ))

    fig.update_layout(
        autosize=False, 
        height=600, 
        width=800,
        title_text=title,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
       
    )   



    return fig
    #fig.show()
    #fig.write_image("fig1.svg", engine="kaleido")
    #fig.write_html("top500.html")