from flask import Flask
from dash import Dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
from preprocess import load_and_preprocess_data, get_goal_distribution_df
from graphs import create_offensive_3d_scatter_plot, create_defensive_3d_scatter_plot, create_parallel_coordinates_plot, create_goal_dist_bar_chart, create_radar_chart
import os

server = Flask(__name__)

app = Dash(__name__, server=server, url_base_pathname='/dash/', suppress_callback_exceptions=True)

with open('templates/index.html', 'r') as file:
    index_string = file.read()

# Assign index_string to app.index_string
app.index = index_string
file_path = os.path.join(os.path.dirname(__file__), 'static', 'EURO_2020_DATA.xlsx')

team_stats = load_and_preprocess_data(file_path)
goal_dist = get_goal_distribution_df(file_path)

app.layout = html.Div([
    html.H1("UEFA Euro 2020 Team Performance in 3D", style={'textAlign': 'center', 'padding': '20px'}),
    html.Div([
        html.Label("Select a team:", style={'padding': '10px'}),
        dcc.Dropdown(
            id='team-dropdown',
            options=[{'label': team, 'value': team} for team in team_stats['TeamName'].unique()],
            value='Italy',
            style={'width': '95%'}
        ),
    ], style={'display': 'flex', 'padding': '10px'}),
    
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Offensive Performance', value='tab-1', style={'padding': '10px'}),
        dcc.Tab(label='Defensive Performance', value='tab-2', style={'padding': '10px'}),
        dcc.Tab(id='parallel-coordinates',label='Parallel Coordinates', value='tab-3', style={'padding': '10px'}),
        dcc.Tab(label='Radar Chart', value='tab-4', style={'padding': '10px'}),
        dcc.Tab(label='Goal distribution', value='tab-5', style={'padding': '10px'}),
    ]),
    dcc.Graph(id='graph-content', style={'height': '80vh', 'width': '100%'}),
    html.Div(id='hover-data')
])

@app.callback(Output('graph-content', 'figure'),
              [Input('tabs-example', 'value'),
               Input('team-dropdown', 'value')])
def render_content(tab, selected_team):
    if tab == 'tab-1':
        return create_offensive_3d_scatter_plot(team_stats)
    elif tab == 'tab-2':
        return create_defensive_3d_scatter_plot(team_stats)
    elif tab == 'tab-3':
        return create_parallel_coordinates_plot(team_stats,selected_team)
    elif tab == 'tab-4':
        return create_radar_chart(team_stats, selected_team)
    elif tab == 'tab-5':
        return create_goal_dist_bar_chart(goal_dist, selected_team)

if __name__ == '__main__':
    app.run_server(debug=True)
