import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output

from app import app

data = pd.read_csv("WASH_Sanitation.csv")

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
            dcc.Link('Country wise Improvements', href='/country-sanitation', className="tabfirst"),
            dcc.Link('Mean Population Analysis', href='/mean-service', className="tab"),
            dcc.Link('Water service Coverage', href='/median-service', className="tab"),
            dcc.Link('Mortality Rate Vs Service Level', href='/comparison', className="tab"),
            dcc.Link('Mortality Rate Prediction', href='/prediction', className="tab"),
        ]  
        ),
        html.Div(
            children=[
                html.Div(children="Country", className="menu-title"),
                dcc.Dropdown(
                    id="region-filter",
                    options=[
                        {"label": Country, "value": Country}
                        for Country in np.sort(data.Country.unique())
                    ],
                    value="Afghanistan",
                    clearable=False,
                    className="dropdown"
                ),
            ],
        className="menu"
        ),  
        
        html.Div(
            children=[
              html.Div(
                     children=dcc.Graph(
                        id="san_fig", config={"displayModeBar": False},
                     ),
                    className="card",
                 ),
             
              ],
          className="wrapper",
        ),
    ]
)
@app.callback(
    Output("san_fig", "figure"), 
    Input("region-filter", "value"),
)
def update_charts(Country):
    mask = (
        (data.Country == Country)
    )
    filtered_data = data.loc[mask, :]
    df_long=pd.melt(filtered_data, id_vars=['Year'], value_vars=['Basic service', 'Limited service', 'Safely managed service','Surface water','Unimproved'])
    fig = px.line(
        df_long, x='Year', y='value', color='variable',
        labels={
                     "Year": "Year",
                     "value": "Percentage Coverage",
                     "variable": "Service Level"
                 },
                title="Plot of water service level for the selected country")
    return fig