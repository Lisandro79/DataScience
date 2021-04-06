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
        # dcc.Graph(figure=fig_map, className='card'),
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
    df_council = ds.select_council(year=selected_year, election_type='municipales', council=council)
    data, political_parties = ds.transpose_table(df_council, selected_year)
    options = [{'label': i, 'value': i} for i in political_parties]
    serialized_data = data.to_json(date_format='iso', orient='split')
    return serialized_data, json.dumps(political_parties), options, options, \
           political_parties[0], political_parties[1], political_parties[0], options


@app.callback(
    [Output('pie_chart', 'figure'),
     Output('hbar', 'figure')],
    [Input('intermediate-data', 'children'),
     Input('intermediate-parties', 'children'),
     Input('dropdown-hbar', 'value')]
)
def update_pie_bar_charts(serialized_data, serialized_political_parties, dropdown):
    data = pd.read_json(serialized_data, orient='split')
    political_parties = json.loads(serialized_political_parties)
    results = pd.DataFrame(data[political_parties].mean(axis=0).reset_index())
    results.columns = ['Partidos Politicos', 'Porcentage Votos']
    results.sort_values(by=['Porcentage Votos'], ascending=False, inplace=True)
    results.reset_index(drop=True, inplace=True)

    fig_pie = px.pie(results, values='Porcentage Votos', names='Partidos Politicos')
    fig_pie.update_layout()

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
                     height=800,
                     # width=1600,
                     title='Pilar')
    fig_bar.update_layout(plot_bgcolor=colors['background'],
                          paper_bgcolor=colors['background'],
                          font_color=colors['text']
                          )

    return fig_pie, fig_bar


@app.callback(
    Output('scatter', 'figure'),
    [Input('intermediate-data', 'children'),
     Input('dropdown-scatter1', 'value'),
     Input('dropdown-scatter2', 'value')]
)
def update_scatter(serialized_data, dropdown1, dropdown2):
    data = pd.read_json(serialized_data, orient='split')
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
    return fig_scatter


if __name__ == "__main__":
    app.run_server(debug=True)

# Fix: when year changes, all graphs should update. Separate the callbacks
# Agregar dropdown menu para hacer sorting del bar chart


# time1 = perf_counter()
# time2 = perf_counter()
# print(f"Year {selected_year}, Took {time2 - time1} seconds")


# Map
# counties = {features['properties']['nombre']: random.randint(0, 300) for features in geojson['features']}
# df = pd.DataFrame(list(counties.items()), columns=['Municipios', 'Votes'])
#
# counties_pilar = {features['properties']['nombre']: random.randint(0, 300) for features in geojson_pilar['features']}
# df_pilar = pd.DataFrame(list(counties_pilar.items()), columns=['Localidad', 'Votes'])
#
# fig_map = px.choropleth_mapbox(df, geojson=geojson, color="Votes",
#                                locations="Municipios", featureidkey="properties.nombre",
#                                center={"lat": LOC_PILAR[0], "lon": LOC_PILAR[1]},
#                                mapbox_style="carto-positron", zoom=4, opacity=0.2)


# sortBy = 'FRENTE DE TODOS'

# df = select_municipio(elections, year, election_type, codigo_municipio, invalid_codes)
# df = df.drop(['provincia', 'id_municipio', 'circuito'], axis=1)
# new_data, cols_parties = transpose_table(df, year, partidos_politicos=partidos_politicos)
# results = pd.DataFrame(new_data[cols_parties].mean(axis=0).reset_index())
# results.columns = ['Partidos Politicos', 'Porcentage Votos']
# extra = results.sort_values(by=['Porcentage Votos'], ascending=False)
# extra.reset_index(drop=True, inplace=True)


# LOC_PILAR = [-34.466667, -58.916667]
# LOC_BsAs = [-35.828117, -59.811962]
