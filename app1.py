# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 00:01:26 2018

@author: TT
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

def getLayout():
    return html.Div([
        html.H3('App 1'),
        dcc.Dropdown(
            id='app-1-dropdown',
            options=[
                {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                    'NYC', 'MTL', 'LA'
                ]
            ]
        ),
        html.Div(id='app-1-display-value'),
        dcc.Link('Go Back', href='/')
    ])


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)