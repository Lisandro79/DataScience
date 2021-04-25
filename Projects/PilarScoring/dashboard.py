import plotly.express as px
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from data_source import DataSource
from time import perf_counter
import json
import random

# Select initial Municipio and voting booths, Filter valid votes
ds = DataSource()
council = 'PILAR'
df = ds.select_council(year=2019, election_type='municipales', council=council)
parties = ds.get_council_parties(2019, vote_ids=df.codigo_voto.unique())

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
fig_map = px.choropleth_mapbox(dat, geojson=geojson, color="Votes",
                               locations="Municipios", featureidkey="properties.nombre",
                               center={"lat": LOC_PILAR[0], "lon": LOC_PILAR[1]},
                               mapbox_style="carto-positron", zoom=4, opacity=0.2)
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
                   value=2019, min=2015, max=2019, step=4,
                   marks={2015: '2015',
                          2019: '2019'}),
        dcc.Graph(id='pie_chart'),
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
        html.Div(id='intermediate-parties', style={'display': 'none'}),
    ]
)


@app.callback(
    [Output('intermediate-data', 'children'),
     Output('intermediate-parties', 'children'),
     Output('dropdown-scatter1', 'options'),
     Output('dropdown-scatter2', 'options'),
     Output('dropdown-scatter1', 'value'),
     Output('dropdown-scatter2', 'value'),
     Output('dropdown-hbar', 'value'),
     Output('dropdown-hbar', 'options')],
    Input('slider-year', 'value')
)
def update_dataframe(selected_year):
    time1 = perf_counter()
    df_council = ds.select_council(year=selected_year, election_type='municipales', council=council)
    time2 = perf_counter()
    data, political_parties = ds.transpose_table(df_council, selected_year)
    time3 = perf_counter()
    options = [{'label': i, 'value': i} for i in political_parties]
    serialized_data = data.to_json(date_format='iso', orient='split')
    time4 = perf_counter()
    print(f"Select Council {selected_year}, Took {time2 - time1} seconds")
    print(f"Transpose table took {time3-time2}")
    print(f"Serialization Took {time4 - time3}")
    return serialized_data, json.dumps(political_parties), options, options, \
           political_parties[0], political_parties[1], political_parties[0], options


@app.callback(
    [Output('pie_chart', 'figure'),
     Output('scatter', 'figure'),
     Output('hbar', 'figure')],  #  Output('map', 'figure')
    [Input('intermediate-data', 'children'),
     Input('intermediate-parties', 'children'),
     Input('dropdown-scatter1', 'value'),
     Input('dropdown-scatter2', 'value'),
     Input('dropdown-hbar', 'value')]
)
def update_pie_bar_charts(serialized_data, serialized_political_parties,
                          dropdown1, dropdown2, dropdown):
    data = pd.read_json(serialized_data, orient='split')
    political_parties = json.loads(serialized_political_parties)
    results = pd.DataFrame(data[political_parties].mean(axis=0).reset_index())
    results.columns = ['Partidos Politicos', 'Porcentage Votos']
    results.sort_values(by=['Porcentage Votos'], ascending=False, inplace=True)
    results.reset_index(drop=True, inplace=True)

    fig_pie = px.pie(results, values='Porcentage Votos', names='Partidos Politicos')
    fig_pie.update_layout()

    pearson_r = data[dropdown1].corr(data[dropdown2])
    fig_scatter = px.scatter(data,
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
    sorted_by_winner = data.sort_values(by=[dropdown], ascending=False)
    fig_bar = px.bar(sorted_by_winner,
                     x=political_parties,
                     y=np.arange(0, len(data)),
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

    return fig_pie, fig_scatter, fig_bar


if __name__ == "__main__":
    app.run_server(debug=True)

# TODO
#  1. Filter voting booths from villa rosa
#  2. Calculate mean age & gender for each voting booth
#  3. Plot correlation age & gender over
#  Ranking of Voting booths according to volatility (change of vote 2015 - 2019, peronista vs no peronista)
#  Add new page to the dashboard. Navigate through pages
#  Sex, gender, age, school (geographic location), surname (do people with the same surname tend to vote the same?)
#  What can we do with the scoring for each individual?
#  Each variable will have a weight for each voting booth. We can then assign those weights to the individuals. If we
#  could cross these features with external features (e.g., twitter feed)
#  If we could identify the people that vote for the opposite party in voting booths that are volatile, how could
#  a campaign proceed?
