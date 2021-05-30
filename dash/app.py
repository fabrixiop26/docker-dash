import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import plotly.graph_objs as go

app = dash.Dash(__name__)

# ---------- Import and clean data (importing csv into pandas)
df = pd.read_csv("intro_bees.csv")
df = df.groupby(['state', 'ansi', 'affected_by', 'year', 'state_code'])[['pct_of_colonies_impacted']].mean()
df.reset_index(inplace=True)
bee_killers = ["Disease", "Other", "Pesticides", "Pests_excl_Varroa", "Unknown", "Varroa_mites"]
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),
    #Mapa
    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018}],
                 multi=False,
                 value=2015,
                 style={'padding':"15px",'border-radius':"50px",'display': "flex", 'align-items': "center", 'justify-content': "center"}
                 ),
            
    html.Br(),
    html.Div(id='output_container', children=[],style={'text-align': 'center'}),
    html.Br(),
    dcc.Graph(id='my_bee_map', figure={},style={'border-radius':"50px"}),
    html.Br(),
    #Barras
    dcc.Dropdown(id="slct_year2",
                    options=[
                        {"label": "2015", "value": 2015},
                        {"label": "2016", "value": 2016},
                        {"label": "2017", "value": 2017},
                        {"label": "2018", "value": 2018}],
                    multi=False,
                    value=2015,
                    style={'padding':"15px",'border-radius':"50px",'display': "flex", 'align-items': "center", 'justify-content': "center"}
                    ),
                
    html.Br(),
    html.Div(id='output_container2', children=[],style={'text-align': 'center'}),
    html.Br(),
    dcc.Graph(id='my_bee_map2', figure={}),
    
    html.Br(),
    #Lineas
    dcc.Dropdown(id="slct_impact3",
                 options=[{"label": x, "value":x} for x in bee_killers],
                 value="Pesticides",
                 multi=False,
                 style={'transform': "translate(70%)",'border-radius':"50px",'width':"40%"}),
            
    html.Br(),
    html.Div(id='output_container3', children=[],style={'text-align': 'center'}),
    html.Br(),
    dcc.Graph(id='my_bee_map3', figure={})


]
)

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):
    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["year"] == option_slctd]
    dff = dff[dff["affected_by"] == "Varroa_mites"]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='pct_of_colonies_impacted',
        hover_data=['state', 'pct_of_colonies_impacted'],
        color_continuous_scale=px.colors.sequential.Purpor,
        labels={'pct_of_colonies_impacted': '% of Bee Colonies'},
        template='plotly'
    )
    fig.layout.plot_bgcolor = '#e7fcf7'
    fig.layout.paper_bgcolor = '#e7fcf7'
    return container, fig 
@app.callback(
    [Output(component_id='output_container2', component_property='children'),
     Output(component_id='my_bee_map2', component_property='figure')],
    [Input(component_id='slct_year2', component_property='value')]
)
def update_graph2(option_slctd):

    container2 = "The year chosen by user was: {}".format(option_slctd)

    dff2 = df.copy()
    dff2 = dff2[dff2["year"] == option_slctd]
    dff2 = dff2[dff2["affected_by"] == "Varroa_mites"]

    fig2 = px.bar(
        data_frame=dff2,
        x='state',
        y='pct_of_colonies_impacted',
        hover_data=['state', 'pct_of_colonies_impacted'],
        labels={'pct_of_colonies_impacted': '% of Bee Colonies'},
        template='plotly'
    )

    return container2, fig2

@app.callback(
    [Output(component_id='output_container3', component_property='children'),
     Output(component_id='my_bee_map3', component_property='figure')],
    [Input(component_id='slct_impact3', component_property='value')]
)

def update_graph3(option_slctd):

    container3 = "The bee-killer chosen by user was: {}".format(option_slctd)

    dff3 = df.copy()
    dff3 = dff3[dff3["affected_by"] == option_slctd]
    dff3 = dff3[(dff3["state"] == "Idaho") | (dff3["state"] == "New York") | (dff3["state"] == "New Mexico")]

    fig3 = px.line(
        data_frame=dff3,
        x='year',
        y='pct_of_colonies_impacted',
        color='state',
        template='plotly'
    )

    return container3, fig3


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(host="localhost", port=8080,debug=True)
