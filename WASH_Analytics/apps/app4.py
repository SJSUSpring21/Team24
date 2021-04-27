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
    yaxis_title="Service level",
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
            dcc.Link('WASH Home', href='/wash-home', className="tab"),
            dcc.Link('Country wise Sanitation', href='/country-sanitation', className="tab"),
            dcc.Link('Mean water service level', href='/mean-service', className="tab"),
            dcc.Link('Median water service level', href='/median-service', className="tab first"),
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

