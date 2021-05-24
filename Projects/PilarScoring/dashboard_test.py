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
from time import perf_counter
import dash_bootstrap_components as dbc


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
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Dashboard Nous'

# Layout
app.layout = dbc.Container(
    children=[
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), width=4),
                dbc.Col(html.Div("One of three columns"), width=4),
                dbc.Col(html.Div("One of three columns"), width=4),
            ], align='center'
        ),
    ], fluid=True
)


if __name__ == "__main__":
    app.run_server(debug=True)

#
# @app.callback(
#     [Output('intermediate-data', 'children'),
#      Output('intermediate-volatility', 'children'),
#      Output('intermediate-parties', 'children'),
#      Output('dropdown-localidad', 'options'),
#      Output('dropdown-localidad-partidos', 'options'),
#      Output('dropdown-localidad-features', 'options'),
#      Output('dropdown_county_volatility', 'options'),
#      Output('dropdown_county_parties', 'options'),
#      Output('dropdown-localidad', 'value'),
#      Output('dropdown-localidad-partidos', 'value'),
#      Output('dropdown-localidad-features', 'value'),
#      Output('dropdown_county_volatility', 'value'),
#      Output('dropdown_county_parties', 'value'),
#      Output('dropdown-scatter1', 'options'),
#      Output('dropdown-scatter2', 'options'),
#      Output('dropdown-scatter1', 'value'),
#      Output('dropdown-scatter2', 'value'),
#      Output('dropdown-hbar', 'value'),
#      Output('dropdown-hbar', 'options')],
#     Input('slider-year', 'value')
# )
# def update_dataframe(selected_year):
#     general_election, _, volatility, political_parties = ds.select_council(year=selected_year,
#                                                                            election_type='municipales',
#                                                                            council=council)
#     formatted_localidades = [{'label': i, 'value': i} for i in ds.electoral_roll.localidad.unique()]
#     formatted_features = [{'label': i, 'value': i} for i in ds.electoral_roll.columns[2:]]
#     formatted_political_parties = [{'label': i, 'value': i} for i in political_parties]
#
#     return general_election.to_json(date_format='iso', orient='split'), \
#            volatility.to_json(date_format='iso', orient='split'), \
#            json.dumps(political_parties), \
#            formatted_localidades, \
#            formatted_political_parties, \
#            formatted_features, \
#            formatted_localidades, \
#            formatted_political_parties, \
#            localidades[0], \
#            political_parties[1], \
#            features[0], \
#            localidades[0], \
#            political_parties[1], \
#            formatted_political_parties, \
#            formatted_political_parties, \
#            political_parties[1], \
#            political_parties[3], \
#            political_parties[1], \
#            formatted_political_parties
#
#
# @app.callback(Output('fig_volatility', 'figure'),
#               [Input('intermediate-data', 'children'),
#                Input('intermediate-parties', 'children'),
#                Input('intermediate-volatility', 'children'),
#                Input('dropdown_county_volatility', 'value'),
#                Input('dropdown_county_parties', 'value')])
# def update_volatility_chart(serialized_data,
#                             serialized_political_parties,
#                             serialized_volatility,
#                             dropdown_county_volatility,
#                             dropdown_volatility_political_party):
#     # time1 = perf_counter()
#     general_election = pd.read_json(serialized_data, orient='split')
#     political_parties = json.loads(serialized_political_parties)
#     election_volatility = pd.read_json(serialized_volatility, orient='split')
#     volatility_filtered_by_county = election_volatility.loc[general_election['localidad'] == dropdown_county_volatility]
#     # time2 = perf_counter()
#     # print(f'Took {time2 - time1}')
#     fig_volatility = px.scatter(volatility_filtered_by_county,
#                                 x=dropdown_volatility_political_party,
#                                 y=political_parties[3],
#                                 hover_data=['mesa'])
#     return fig_volatility
#
#
# @app.callback(
#     [Output('pie_chart', 'figure'),
#      Output('scatter', 'figure'),
#      Output('hbar', 'figure'),
#      Output('scatter-localidad', 'figure'),
#      Output('fig_bar_localidad', 'figure')],
#     [Input('intermediate-data', 'children'),
#      Input('intermediate-volatility', 'children'),
#      Input('intermediate-parties', 'children'),
#      Input('dropdown-localidad', 'value'),
#      Input('dropdown-localidad-partidos', 'value'),
#      Input('dropdown-localidad-features', 'value'),
#      Input('dropdown_county_volatility', 'value'),
#      Input('dropdown_county_parties', 'value'),
#      Input('dropdown-scatter1', 'value'),
#      Input('dropdown-scatter2', 'value'),
#      Input('dropdown-hbar', 'value')]
# )
# def update_pie_bar_charts(serialized_data,
#                           serialized_volatility,
#                           serialized_political_parties,
#                           dropdown_localidad,
#                           dropdown_localidad_partido,
#                           dropdown_localidad_feature,
#                           dropdown_county_volatility,
#                           dropdown_volatility_political_party,
#                           dropdown1,
#                           dropdown2,
#                           dropdown):
#     general_election = pd.read_json(serialized_data, orient='split')
#     political_parties = json.loads(serialized_political_parties)
#     results = pd.DataFrame(general_election[political_parties].mean(axis=0).reset_index())
#     results.columns = ['Partidos Politicos', 'Porcentage Votos']
#     results.sort_values(by=['Porcentage Votos'], ascending=False, inplace=True)
#     results.reset_index(drop=True, inplace=True)
#
#     fig_pie = px.pie(results, values='Porcentage Votos', names='Partidos Politicos')
#     fig_pie.update_layout()
#
#     filtered_by_county = general_election.loc[general_election['localidad'] == dropdown_localidad]
#     pearson_r = filtered_by_county[dropdown_localidad_feature] \
#         .corr(filtered_by_county[dropdown_localidad_partido])
#     fig_scatter_localidad = px.scatter(filtered_by_county,
#                                        x=dropdown_localidad_feature,
#                                        y=dropdown_localidad_partido,
#                                        hover_data=['mesa'],
#                                        color=dropdown2,
#                                        title=f"Pearson's R: {pearson_r}")
#     fig_scatter_localidad.update_layout(plot_bgcolor=colors['background'],
#                                         paper_bgcolor=colors['background'],
#                                         font_color=colors['text']
#                                         )
#
#     sorted_by_winner = filtered_by_county.sort_values(by=[dropdown_localidad_feature])
#     fig_bar_localidad = px.bar(sorted_by_winner,
#                                x=political_parties,
#                                y=np.arange(0, len(filtered_by_county)),
#                                orientation='h',
#                                barmode="stack",
#                                opacity=1,
#                                hover_data=["mesa", dropdown_localidad_feature],
#                                labels={'value': "Porcentage Votos", 'y': '', 'variable': 'Partidos Politicos'},
#                                # color_discrete_sequence= px.colors.qualitative.G10,
#                                color_discrete_sequence=["red", "blue", "yellow", "green", "magenta", "goldenrod"],
#                                height=800)
#     fig_bar_localidad.update_layout(plot_bgcolor=colors['background'],
#                                     paper_bgcolor=colors['background'],
#                                     font_color=colors['text']
#                                     )
#
#     pearson_r = general_election[dropdown1].corr(general_election[dropdown2])
#     fig_scatter = px.scatter(general_election,
#                              x=dropdown1,
#                              y=dropdown2,
#                              hover_data=['mesa'],
#                              color=dropdown2,
#                              title=f"Pearson's R: {pearson_r}")
#     fig_scatter.update_layout(plot_bgcolor=colors['background'],
#                               paper_bgcolor=colors['background'],
#                               font_color=colors['text']
#                               )
#
#     # Voting Booths, horizontal bar plot
#     sorted_by_winner = general_election.sort_values(by=[dropdown])
#     fig_bar = px.bar(sorted_by_winner,
#                      x=political_parties,
#                      y=np.arange(0, len(general_election)),
#                      orientation='h',
#                      barmode="stack",
#                      opacity=1,
#                      hover_data=["mesa"],
#                      labels={'value': "Porcentage Votos", 'y': '', 'variable': 'Partidos Politicos'},
#                      # color_discrete_sequence= px.colors.qualitative.G10,
#                      color_discrete_sequence=["red", "blue", "yellow", "green", "magenta", "goldenrod"],
#                      height=800)
#     fig_bar.update_layout(plot_bgcolor=colors['background'],
#                           paper_bgcolor=colors['background'],
#                           font_color=colors['text']
#                           )
#
#     return fig_pie, fig_scatter, fig_bar, fig_scatter_localidad, fig_bar_localidad

