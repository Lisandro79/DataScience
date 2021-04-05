import plotly.express as px
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from data_source import DataSource


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
                className="header-title",),
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
        dcc.Graph(id='hbar', className='card'),
        # dcc.Graph(figure=fig_map, className='card'),
    ]
)


@app.callback(
    [Output('pie_chart', 'figure'), Output('scatter', 'figure'), Output('hbar', 'figure')],
    [Input('slider-year', 'value'), Input('dropdown-scatter1', 'value'), Input('dropdown-scatter2', 'value')]
)
def update_charts(selected_year, dropdown1, dropdown2):
    dataset = ds.select_council(year=selected_year, election_type='municipales', council=council)
    new_data, cols_parties = ds.transpose_table(dataset, selected_year)

    results = pd.DataFrame(new_data[cols_parties].mean(axis=0).reset_index())
    results.columns = ['Partidos Politicos', 'Porcentage Votos']
    results.sort_values(by=['Porcentage Votos'], ascending=False, inplace=True)
    results.reset_index(drop=True, inplace=True)
    # new_data.sort_values([sortBy], ascending=True, inplace=True)

    fig_pie = px.pie(results, values='Porcentage Votos', names='Partidos Politicos', title='Resultado Final')

    fig_pie.update_layout(transition_duration=200)

    # Voting Booths, horizontal bar plot
    fig_bar = px.bar(new_data,
                     x=cols_parties,
                     y=np.arange(0, len(new_data)),
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

    # scatter plot to compare booths
    first = dropdown1  # results['Partidos Politicos'][0]
    second = dropdown2  # results['Partidos Politicos'][1]
    pearson_r = new_data[first].corr(new_data[second])
    fig_scatter = px.scatter(new_data,
                             x=first,
                             y=second,
                             hover_data=['mesa'],
                             color=second,
                             title=f"Pearson's R: {pearson_r}")

    fig_scatter.update_layout(plot_bgcolor=colors['background'],
                              paper_bgcolor=colors['background'],
                              font_color=colors['text']
                              )

    return fig_pie, fig_scatter, fig_bar


if __name__ == "__main__":
    app.run_server(debug=True)


# Agregar dropdown menu para elegir partido en el scatter plot
# Agregar dropdown menu para ordenar el bar chart

# Why don't we have Municipales 2011?


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
#
# first = extra['Partidos Politicos'][0]
# second = extra['Partidos Politicos'][1]



# Main results of the election
# results = pd.DataFrame(new_data[cols_parties].mean(axis=0).reset_index())
# results.columns = ['Partidos Politicos', 'Porcentage Votos']


#
# LOC_PILAR = [-34.466667, -58.916667]
# LOC_BsAs = [-35.828117, -59.811962]
