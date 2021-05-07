import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app import app

data = pd.read_csv("WASH.csv")

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
                dcc.Link('Unsafe WASH Mortality Rate', href='/wash-home', className="tab first"),
                dcc.Link('Country wise Improvements', href='/country-sanitation', className="tab"),
                dcc.Link('Mean Population Analysis', href='/mean-service', className="tabfirst"),
                dcc.Link('Water service Coverage', href='/median-service', className="tab"),
                dcc.Link('Mortality Rate Vs Service Level', href='/comparison', className="tab"),
                dcc.Link('Mortality Rate Prediction', href='/prediction', className="tab"),
                ]
            ),
         html.Div(
                children=[
                html.Div(children="Service Level", className="menu-title"),
                dcc.Dropdown(
                    id="service-filter",
                    options=[
                        {"label": ServiceLevel, "value": ServiceLevel}
                        for ServiceLevel in np.sort(data.ServiceLevel.unique())
                    ],
                    value="At least basic",
                    clearable=False,
                    className="dropdown"
                ),
            ],
        className="menu",
        ),  
    html.Div(
            children=[
              html.Div(
                     children=dcc.Graph(
                        id="service_fig", config={"displayModeBar": False},
                     ),
                    className="card",
                 ),
             
              ],
          className="wrapper",
        ),
    ]
)
@app.callback(
    Output("service_fig", "figure"), 
    Input("service-filter", "value"),
)
def update_charts(ServiceLevel):
    mask = (
        (data.ServiceLevel == ServiceLevel)
    )
    filtered_data = data.loc[mask, :]
    df = filtered_data.groupby('Year', as_index=False)['Population'].mean()
    fig  = go.Figure([
            go.Bar(
              y = df.Population,
              x =df.Year
        )])
    fig.update_layout(
    title="Mean of the population with the selected service level by year",
    xaxis_title="Year",
    yaxis_title="Population",
    )
    return fig