import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

from app import app

data = pd.read_csv("WASH.csv")

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="WASH Analytics", className="header-title"),
                html.P(
                      children="Analyze the Water Sanitation and Hygiene data and mortality rate attributed to exposure to unsafe WASH services for different countries",
                    className="header-description"
                     ),
             ],
             className="header",
            ),
        html.Div(children=[
            dcc.Link('WASH Home', href='/wash-home', className="tab first"),
            dcc.Link('Country wise Sanitation', href='/country-sanitation', className="tab"),
            dcc.Link('Mean water service level', href='/mean-service', className="tab"),
            dcc.Link('Median water service level', href='/median-service', className="tab"),
            ]
        ),
        html.Div(
        children=[
             dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Country"],
                        "y": data["Mortality Rate"],
                        "type": "lines",
                    },
                ],
                'layout':{
                'title':'Mortality rate attributed to unsafe WASH services for different countries',
                'xaxis':{
                    'title':'Country'
                },
                'yaxis':{
                     'title':'Mortality rate'
                }
            }
        } 
        ),
        ],className="wrapper",
        )
    ]
)
