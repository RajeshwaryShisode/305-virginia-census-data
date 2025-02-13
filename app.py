import dash
from dash import dcc, html
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd

# Read in the USA counties shape files
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

########### Define a few variables ######

tabtitle = '3D Virginia Counties HW'
sourceurl = 'https://www.kaggle.com/muonneutrino/us-census-demographic-data'
githublink = 'https://github.com/austinlasseter/dash-virginia-counties'
varlist=['TotalPop', 'Men', 'Women', 'Hispanic',
       'White', 'Black', 'Native', 'Asian', 'Pacific', 'VotingAgeCitizen',
       'Income', 'IncomeErr', 'IncomePerCap', 'IncomePerCapErr', 'Poverty',
       'ChildPoverty', 'Professional', 'Service', 'Office', 'Construction',
       'Production', 'Drive', 'Carpool', 'Transit', 'Walk', 'OtherTransp',
       'WorkAtHome', 'MeanCommute', 'Employed', 'PrivateWork', 'PublicWork',
       'SelfEmployed', 'FamilyWork', 'Unemployment', 'RUCC_2013']

df=pd.read_pickle('resources/va-stats.pkl')

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
    html.H1('Virginia Census Data 2017'),
    # Dropdowns
    html.Div(children=[
        # left side
        html.Div([
                html.H6('Select census variable:'),
                dcc.Dropdown(
                    id='stats-drop',
                    options=[{'label': i, 'value': i} for i in varlist],
                    value='MeanCommute'
                ),
        ], className='three columns'),
        # right side
        html.Div([
            dcc.Graph(id='va-map')
        ], className='nine columns'),
    ], className='twelve columns'),

    # Footer
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

############ Callbacks
@app.callback(Output('va-map', 'figure'),
              [Input('stats-drop', 'value')])
def display_results(selected_value):
    valmin=df[selected_value].min()
    valmax=df[selected_value].max()
# https://community.plot.ly/t/what-colorscales-are-available-in-plotly-and-which-are-the-default/2079


    fig = px.scatter_3d(df, x='IncomePerCap', y='Men', z=selected_value, size='TotalPop', color='Women',
                    hover_data=['Office'])
    fig.update_layout(scene_zaxis_type="log")
   

    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
