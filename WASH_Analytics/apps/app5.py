import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
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
                dcc.Link('Unsafe WASH Mortality Rate', href='/', className="tab"),
                dcc.Link('Country wise Improvements', href='/country-sanitation', className="tab"),
                dcc.Link('Mean Population Analysis', href='/mean-service', className="tab"),
                dcc.Link('Water service Coverage', href='/median-service', className="tab"),
                dcc.Link('Mortality Rate Vs Service Level', href='/comparison', className="tabfirst"),
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
                    value="Basic service",
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
                        id="imp_fig", config={"displayModeBar": False},
                     ),
                    className="card",
                 ),
             
              ],
          className="wrapper",
        ),
    ]
)
@app.callback(
    Output("imp_fig", "figure"), 
    Input("service-filter", "value"),
)
def update_charts(ServiceLevel):
    mask = (
        (data.ServiceLevel == ServiceLevel)
    )
    filtered_data = data.loc[mask, :]
    df_filtered_year = filtered_data.loc[filtered_data["Year"] == 2014]
    df_filtered_sex = df_filtered_year.loc[df_filtered_year["Sex"] == 'Both sexes']
    df = df_filtered_sex.groupby(['Country','MortalityRate'], as_index=False)['Coverage'].mean()
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=df.Country,
    y=df.Coverage,
    name='Service level Coverage',
    marker_color='limegreen'
    ))
    fig.add_trace(go.Bar(
    x=df.Country,
    y=df.MortalityRate,
    name='Mortality Rate',
    marker_color='lightsalmon'
    ))
    fig.update_yaxes(tick0=0, dtick=20)
    fig.update_layout(barmode='group', height=700, title="Comparison of different water service levels and mortality rate of different countries",
    xaxis_title="Country",
    yaxis_title="Value")
    return fig