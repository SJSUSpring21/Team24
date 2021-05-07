import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import sklearn
from dash.dependencies import Input, Output
from sklearn.model_selection import train_test_split
from sklearn import linear_model, tree, neighbors
from sklearn.metrics import accuracy_score

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
                dcc.Link('Mortality Rate Vs Service Level', href='/comparison', className="tab"),
                dcc.Link('Mortality Rate Prediction', href='/prediction', className="tabfirst"),
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
                        id="predict_fig", config={"displayModeBar": False},
                     ),
                    className="card",
                 ),
             
              ],
          className="wrapper",
        ),
        html.Div(
            children=[
              html.Div(
                     children=dcc.Graph(
                        id="predict_fig_dt", config={"displayModeBar": False},
                     ),
                    className="card",
                 ),
             
              ],
          className="wrapper",
        ),
        html.Div(
            children=[
              html.Div(
                     children=dcc.Graph(
                        id="predict_fig_knn", config={"displayModeBar": False},
                     ),
                    className="card",
                 ),
             
              ],
          className="wrapper",
        ),
    ]
)
@app.callback(
    [Output("predict_fig", "figure"), Output("predict_fig_dt", "figure"), Output("predict_fig_knn", "figure")],
    Input("service-filter", "value"),
)
def update_charts(ServiceLevel):
    mask = (
        (data.ServiceLevel == ServiceLevel)
    )
    filtered_data = data.loc[mask, :]
    df_filtered_year = filtered_data.loc[filtered_data["Year"] == 2014]
    df = df_filtered_year.loc[df_filtered_year["Sex"] == 'Both sexes']

    X = df.Coverage.values[:, None]
    y = df.MortalityRate
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = linear_model.LinearRegression()
    model.fit(X_train, y_train)
 
    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    predict_fig = go.Figure([
        go.Scatter(x=X_train.squeeze(), y=y_train, 
                   name='Train', mode='markers'),
        go.Scatter(x=X_test.squeeze(), y=y_test, 
                   name='Test', mode='markers'),
        go.Scatter(x=x_range, y=y_range, 
                   name='Prediction')
    ])
    predict_fig.update_layout(height=500,title="Mortality rate prediction with different water service levels : Regression Model",
    xaxis_title="Service level coverage",
    yaxis_title="Mortality Rate",
    title_font_color="#c91b1b",
    )

    model_dt = tree.DecisionTreeRegressor()
    model_dt.fit(X_train, y_train)
 
    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model_dt.predict(x_range.reshape(-1, 1))

    predict_fig_dt = go.Figure([
        go.Scatter(x=X_train.squeeze(), y=y_train, 
                   name='Train', mode='markers'),
        go.Scatter(x=X_test.squeeze(), y=y_test, 
                   name='Test', mode='markers'),
        go.Scatter(x=x_range, y=y_range, 
                   name='Prediction')
    ])
    predict_fig_dt.update_layout(height=500,title="Mortality rate prediction with different water service levels : Decision Tree Model",
    xaxis_title="Service level coverage",
    yaxis_title="Mortality Rate",
    title_font_color="#c91b1b",
    )

    model_knn = neighbors.KNeighborsRegressor()
    model_knn.fit(X_train, y_train)
 
    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model_knn.predict(x_range.reshape(-1, 1))

    predict_fig_knn = go.Figure([
        go.Scatter(x=X_train.squeeze(), y=y_train, 
                   name='Train', mode='markers'),
        go.Scatter(x=X_test.squeeze(), y=y_test, 
                   name='Test', mode='markers'),
        go.Scatter(x=x_range, y=y_range, 
                   name='Prediction')
    ])
    predict_fig_knn.update_layout(height=500,title="Mortality rate prediction with different water service levels : k-NN Model",
    xaxis_title="Service level coverage",
    yaxis_title="Mortality Rate",
    title_font_color="#c91b1b",
    )
    
    return predict_fig, predict_fig_dt, predict_fig_knn