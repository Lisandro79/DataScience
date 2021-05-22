import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from data_source import DataSource
import json
import random

ds = DataSource()
council = 'PILAR'
data, data_paso, volatility, parties = ds.select_council(year=2019,
                                                         election_type='municipales',
                                                         council=council)
localidades = ds.electoral_roll.localidad.unique()
features = ds.electoral_roll.columns[2:]

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Dashboard
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Dashboard Nous'

# Map
LOC_PILAR = [-34.466667, -58.916667]
# LOC_BsAs = [-35.828117, -59.811962]
geojson = ds.get_geo_polygons()
counties = {features['properties']['nombre']: random.randint(0, 300) for features in geojson['features']}
dat = pd.DataFrame(list(counties.items()), columns=['Municipios', 'Votes'])
dat = dat.loc[dat.Municipios.str.upper() == council]
fig_map = px.choropleth_mapbox(dat, geojson=geojson,
                               locations="Municipios", featureidkey="properties.nombre",
                               center={"lat": LOC_PILAR[0], "lon": LOC_PILAR[1]},
                               mapbox_style="carto-positron", zoom=4, opacity=0.2)  # color="Votes",
# Layout
app.layout = html.Div(
    children=[
        html.H1(children=f"Municipio: {council}",
                className="header-title", ),
        html.P(
            children="Analisis de las mesas electorales",
            className="header-description",
        ),
        dcc.Slider(id='slider-year',
                   value=2019, min=2019, max=2019, step=4,
                   marks={2019: '2019'}),
        dcc.Graph(id='pie_chart'),

        html.Div([
            html.Div([dcc.Dropdown(id='dropdown_county_volatility',
                                   options=[{'label': i, 'value': i} for i in localidades],
                                   value=localidades[0]
                                   )
                      ],
                     style={'width': '28%', 'display': 'inline-block'}),
            html.Div([dcc.Dropdown(id='dropdown_county_parties',
                                   options=[{'label': i, 'value': i} for i in parties],
                                   value=parties[0]
                                   )
                      ],
                     style={'width': '28%', 'display': 'inline-block'}),
        ]),
        dcc.Graph(id='fig_volatility', className='card'),

        html.Div([
            html.Div([dcc.Dropdown(id='dropdown-localidad',
                                   options=[{'label': i, 'value': i} for i in localidades],
                                   value=localidades[0]
                                   )
                      ],
                     style={'width': '28%', 'display': 'inline-block'}),
            html.Div([dcc.Dropdown(id='dropdown-localidad-partidos',
                                   options=[{'label': i, 'value': i} for i in parties],
                                   value=parties[0]
                                   )
                      ],
                     style={'width': '28%', 'display': 'inline-block'}),
            html.Div([dcc.Dropdown(id='dropdown-localidad-features',
                                   options=[{'label': i, 'value': i} for i in features],
                                   value=features[0]
                                   )
                      ],
                     style={'width': '38%', 'float': 'right', 'display': 'inline-block'})
        ]),
        dcc.Graph(id='scatter-localidad', className='card'),

        dcc.Graph(id='fig_bar_localidad', className='card'),

        html.Div([
            html.Div([dcc.Dropdown(id='dropdown-scatter1',
                                   options=[{'label': i, 'value': i} for i in parties],
                                   value=parties[0]
                                   )
                      ],
                     style={'width': '48%', 'display': 'inline-block'}),
            html.Div([dcc.Dropdown(id='dropdown-scatter2',
                                   options=[{'label': i, 'value': i} for i in parties],
                                   value=parties[1]
                                   )
                      ],
                     style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),
        dcc.Graph(id='scatter', className='card'),

        html.Div([dcc.Dropdown(id='dropdown-hbar',
                               options=[{'label': i, 'value': i} for i in parties],
                               value=parties[0]
                               )
                  ], style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='hbar', className='card'),

        dcc.Graph(figure=fig_map, className='card'),

        # Hidden div inside the app that stores the intermediate value
        html.Div(id='intermediate-data', style={'display': 'none'}),
        html.Div(id='intermediate-volatility', style={'display': 'none'}),
        html.Div(id='intermediate-parties', style={'display': 'none'}),
    ]
)


@app.callback(
    [Output('intermediate-data', 'children'),
     Output('intermediate-volatility', 'children'),
     Output('intermediate-parties', 'children'),
     Output('dropdown-localidad', 'options'),
     Output('dropdown-localidad-partidos', 'options'),
     Output('dropdown-localidad-features', 'options'),
     Output('dropdown_county_volatility', 'options'),
     Output('dropdown_county_parties', 'options'),
     Output('dropdown-localidad', 'value'),
     Output('dropdown-localidad-partidos', 'value'),
     Output('dropdown-localidad-features', 'value'),
     Output('dropdown_county_volatility', 'value'),
     Output('dropdown_county_parties', 'value'),
     Output('dropdown-scatter1', 'options'),
     Output('dropdown-scatter2', 'options'),
     Output('dropdown-scatter1', 'value'),
     Output('dropdown-scatter2', 'value'),
     Output('dropdown-hbar', 'value'),
     Output('dropdown-hbar', 'options')],
    Input('slider-year', 'value')
)
def update_dataframe(selected_year):
    general_election, _, volatility, political_parties = ds.select_council(year=selected_year,
                                                                           election_type='municipales',
                                                                           council=council)
    formatted_localidades = [{'label': i, 'value': i} for i in ds.electoral_roll.localidad.unique()]
    formatted_features = [{'label': i, 'value': i} for i in ds.electoral_roll.columns[2:]]
    formatted_political_parties = [{'label': i, 'value': i} for i in political_parties]

    return general_election.to_json(date_format='iso', orient='split'), \
           volatility.to_json(date_format='iso', orient='split'), \
           json.dumps(political_parties), \
           formatted_localidades, \
           formatted_political_parties, \
           formatted_features, \
           formatted_localidades, \
           formatted_political_parties, \
           localidades[0], \
           political_parties[0], \
           features[0], \
           localidades[0], \
           political_parties[0], \
           formatted_political_parties, \
           formatted_political_parties, \
           political_parties[0], \
           political_parties[1], \
           political_parties[0], \
           formatted_political_parties


@app.callback(
    [Output('pie_chart', 'figure'),
     Output('fig_volatility', 'figure'),
     Output('scatter', 'figure'),
     Output('hbar', 'figure'),
     Output('scatter-localidad', 'figure'),
     Output('fig_bar_localidad', 'figure')],
    [Input('intermediate-data', 'children'),
     Input('intermediate-volatility', 'children'),
     Input('intermediate-parties', 'children'),
     Input('dropdown-localidad', 'value'),
     Input('dropdown-localidad-partidos', 'value'),
     Input('dropdown-localidad-features', 'value'),
     Input('dropdown_county_volatility', 'value'),
     Input('dropdown_county_parties', 'value'),
     Input('dropdown-scatter1', 'value'),
     Input('dropdown-scatter2', 'value'),
     Input('dropdown-hbar', 'value'), ]
)
def update_pie_bar_charts(serialized_data,
                          serialized_volatility,
                          serialized_political_parties,
                          dropdown_localidad,
                          dropdown_localidad_partido,
                          dropdown_localidad_feature,
                          dropdown_county_volatility,
                          dropdown_volatility_political_party,
                          dropdown1,
                          dropdown2,
                          dropdown):
    general_election = pd.read_json(serialized_data, orient='split')
    election_volatility = pd.read_json(serialized_volatility, orient='split')
    political_parties = json.loads(serialized_political_parties)
    results = pd.DataFrame(general_election[political_parties].mean(axis=0).reset_index())
    results.columns = ['Partidos Politicos', 'Porcentage Votos']
    results.sort_values(by=['Porcentage Votos'], ascending=False, inplace=True)
    results.reset_index(drop=True, inplace=True)

    fig_pie = px.pie(results, values='Porcentage Votos', names='Partidos Politicos')
    fig_pie.update_layout()

    volatility_filtered_by_county = election_volatility.loc[general_election['localidad'] == dropdown_county_volatility]

    # build traces for each x
    traces = {}
    marker_colors = ["red", "blue", "yellow", "green", "magenta", "goldenrod"]
    for idx, col in enumerate(political_parties):
        # TODO: plot scatter & print results of the ordered voting booths with highest difference (FInd School,
        #  geographical information)
        # go.scatter
        traces['trace_' + col] = go.Box(name=col, y=volatility_filtered_by_county[col],
                                        customdata=volatility_filtered_by_county['mesa'],
                                        boxpoints='all',
                                        pointpos=0,
                                        jitter=0.3,
                                        marker=dict(color=marker_colors[idx]),
                                        line=dict(color='rgba(0,0,0,0)'),
                                        fillcolor='rgba(0,0,0,0)')
    # convert data to form required by plotly
    data = list(traces.values())
    # build figure
    fig_volatility = go.Figure(data)

    filtered_by_county = general_election.loc[general_election['localidad'] == dropdown_localidad]
    pearson_r = filtered_by_county[dropdown_localidad_feature] \
        .corr(filtered_by_county[dropdown_localidad_partido])
    fig_scatter_localidad = px.scatter(filtered_by_county,
                                       x=dropdown_localidad_feature,
                                       y=dropdown_localidad_partido,
                                       hover_data=['mesa'],
                                       color=dropdown2,
                                       title=f"Pearson's R: {pearson_r}")
    fig_scatter_localidad.update_layout(plot_bgcolor=colors['background'],
                                        paper_bgcolor=colors['background'],
                                        font_color=colors['text']
                                        )

    sorted_by_winner = filtered_by_county.sort_values(by=[dropdown_localidad_feature])
    fig_bar_localidad = px.bar(sorted_by_winner,
                               x=political_parties,
                               y=np.arange(0, len(filtered_by_county)),
                               orientation='h',
                               barmode="stack",
                               opacity=1,
                               hover_data=["mesa", dropdown_localidad_feature],
                               labels={'value': "Porcentage Votos", 'y': '', 'variable': 'Partidos Politicos'},
                               # color_discrete_sequence= px.colors.qualitative.G10,
                               color_discrete_sequence=["red", "blue", "yellow", "green", "magenta", "goldenrod"],
                               height=800)
    fig_bar_localidad.update_layout(plot_bgcolor=colors['background'],
                                    paper_bgcolor=colors['background'],
                                    font_color=colors['text']
                                    )

    pearson_r = general_election[dropdown1].corr(general_election[dropdown2])
    fig_scatter = px.scatter(general_election,
                             x=dropdown1,
                             y=dropdown2,
                             hover_data=['mesa'],
                             color=dropdown2,
                             title=f"Pearson's R: {pearson_r}")
    fig_scatter.update_layout(plot_bgcolor=colors['background'],
                              paper_bgcolor=colors['background'],
                              font_color=colors['text']
                              )

    # Voting Booths, horizontal bar plot
    sorted_by_winner = general_election.sort_values(by=[dropdown])
    fig_bar = px.bar(sorted_by_winner,
                     x=political_parties,
                     y=np.arange(0, len(general_election)),
                     orientation='h',
                     barmode="stack",
                     opacity=1,
                     hover_data=["mesa"],
                     labels={'value': "Porcentage Votos", 'y': '', 'variable': 'Partidos Politicos'},
                     # color_discrete_sequence= px.colors.qualitative.G10,
                     color_discrete_sequence=["red", "blue", "yellow", "green", "magenta", "goldenrod"],
                     height=800)
    fig_bar.update_layout(plot_bgcolor=colors['background'],
                          paper_bgcolor=colors['background'],
                          font_color=colors['text']
                          )

    return fig_pie, fig_volatility, fig_scatter, fig_bar, fig_scatter_localidad, fig_bar_localidad


if __name__ == "__main__":
    app.run_server(debug=True)
