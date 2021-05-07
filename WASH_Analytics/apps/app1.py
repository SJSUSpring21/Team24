import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app import app

data = pd.read_csv("WASH.csv")
df_new = data.loc[data["Year"] == 2014]
df2 = df_new.loc[df_new["Sex"] == 'Both sexes']
df = df2.groupby(['Country'], as_index=False)['MortalityRate'].mean()
fig  = go.Figure([
            go.Bar(
              y = df.MortalityRate,
              x = df.Country,
        )])
fig.update_layout(
    title="Mortality rate attributed to unsafe WASH services for different countries",
    xaxis_title="Country",
    yaxis_title="Mortality rate",
    height=700,
)
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
            dcc.Link('Unsafe WASH Mortality Rate', href='/', className="tabfirst"),
            dcc.Link('Country wise Improvements', href='/country-sanitation', className="tab"),
            dcc.Link('Mean Population Analysis', href='/mean-service', className="tab"),
            dcc.Link('Water service Coverage', href='/median-service', className="tab"),
            dcc.Link('Mortality Rate Vs Service Level', href='/comparison', className="tab"),
            dcc.Link('Mortality Rate Prediction', href='/prediction', className="tab"),
            ]
        ),
        html.Div(
        children=[
             dcc.Graph(
            figure= fig
        )
        ],className="wrapper",
        )
    ]
)
