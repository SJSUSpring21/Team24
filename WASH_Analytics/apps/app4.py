import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app import app

data = pd.read_csv("WASH_Sanitation.csv")
median = data.groupby('Year',as_index=False)[['Safely managed service', 'Basic service', 'Limited service','Unimproved', 'Surface water']].median()
df = pd.DataFrame(median).set_index('Year')
res = []
for col in df.columns:
    res.append(
        go.Bar(
            x=df.index.values.tolist(),
            y=df[col].values.tolist(),
            name=col
        )
    )

layout = go.Layout(
    barmode='group',
    title="Median of different water services by year",
    xaxis_title="Year",
    yaxis_title="Service level coverage",
)
fig = go.Figure(data=res, layout=layout)

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="WASH Analytics", className="header-title"),
                html.P(
                      children="Analyze the Water Sanitation and Hygiene data and mortality rate of different countries",
                    className="header-description"
                     ),
             ],
             className="header",
            ),
        html.Div(children=[
            dcc.Link('Unsafe WASH Mortality Rate', href='/', className="tab"),
            dcc.Link('Country wise Improvements', href='/country-sanitation', className="tab"),
            dcc.Link('Mean Population Analysis', href='/mean-service', className="tab"),
            dcc.Link('Water service Coverage', href='/median-service', className="tabfirst"),
            dcc.Link('Mortality Rate Vs Service Level', href='/comparison', className="tab"),
            dcc.Link('Mortality Rate Prediction', href='/prediction', className="tab"),
            ]
        ),
        html.Div(
            children=[
              html.Div(
                     children=dcc.Graph(
                        figure  = fig
                )
              )
            ]
          )
    ]
)

