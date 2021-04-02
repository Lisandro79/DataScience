import plotly.express as px
import json
import random
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html


def order_by_column(dataset, col):
    """ Set the selected column in order and returned it first for plotting """
    cols = dataset.columns
    if col not in cols:
        print('Column not in dataset')
        return


def select_municipio(df, year, election_type, codigo_municipio, invalid_codes):
    return df.loc[(df['cargo'] == election_type) &
                  (df['id_municipio'] == codigo_municipio) &
                  (df['year'] == year) &
                  (~df['codigo_voto'].isin(invalid_codes))]


def transpose_table(df, year, partidos_politicos):
    voting_booths = df.mesa.unique()
    parties = df['codigo_voto'].unique()
    cols_parties = [get_party_name(year, partidos_politicos, party) for party in parties]

    res = np.empty((len(voting_booths), len(parties) + 2), dtype=np.int32)
    for index, boot in enumerate(voting_booths):
        col = 0
        data = df.loc[df['mesa'] == boot]
        res[index, col] = boot
        col += 1
        for row in data.iterrows():
            res[index, col] = row[1][4]
            col += 1
        res[index, col] = data.cant_votos.sum()

    dataset = pd.DataFrame(res)
    dataset.columns = np.concatenate((['mesa'], cols_parties, ['total']))

    dataset.loc[:, cols_parties] = dataset.loc[:, cols_parties].div(dataset.loc[:, 'total'], axis=0)
    # dataset = dataset.loc[dataset['mesa'] < 9000]
    return dataset, cols_parties


def get_party_name(year, partidos_politicos, codigo_voto):
    result = partidos_politicos[(partidos_politicos['codigo_voto'] == codigo_voto) &
                                (partidos_politicos['anio'] == year)]['nombre_partido'].values
    if not result:
        print("Partido not found")
        return 'None'
    else:
        return result[0]


def get_municipio_id(municipios_df, municipio):
    result = municipios_df[municipios_df['municipio'] == municipio]['id_municipio'].values
    if not result:
        print("Municipio not found")
        return None
    else:
        return result[0]


with open('./buenos_aires.geojson') as f:
    geojson = json.load(f)

with open('./LocalidadesPilar.json') as localidades:
    geojson_pilar = json.load(localidades)

# Load data
elections = pd.read_csv('./dataset/agregados/Nuevo_elecciones_09_19.csv')
elections.columns = ['year', 'cargo', 'provincia', 'id_municipio', 'circuito', 'mesa', 'codigo_voto', 'cant_votos']

partidos_politicos = pd.read_csv('./dataset/agregados/Nuevo_codigo_votos_09_19.csv')
columns = ['anio', 'codigo_voto', 'nombre_partido']
partidos_politicos.columns = columns

municipios_df = pd.read_csv('./dataset/agregados/municipios_aglo.csv')
municipios_df.columns = ['id_municipio', 'provincia', 'id_aglomerado', 'municipio']

# Select Municipio and voting booths, Filter valid votes
invalid_codes = ['9001', '9002', '9003', '9004', '9005', '9005', '9010', '9020']
municipio = 'PILAR'
codigo_municipio = get_municipio_id(municipios_df, municipio)
year = 2019
election_type = 'municipales'
sortBy = 'FRENTE DE TODOS'

df = select_municipio(elections, year, election_type, codigo_municipio, invalid_codes)
df = df.drop(['provincia', 'id_municipio', 'circuito'], axis=1)
new_data, cols_parties = transpose_table(df, year, partidos_politicos=partidos_politicos)

new_data.sort_values([sortBy], ascending=True, inplace=True)

LOC_PILAR = [-34.466667, -58.916667]
LOC_BsAs = [-35.828117, -59.811962]

# Main results of the election
results = pd.DataFrame(new_data[cols_parties].mean(axis=0).reset_index())
results.columns = ['Partidos Politicos', 'Porcentage Votos']

# Pie chart
fig_results = px.pie(results, values='Porcentage Votos', names='Partidos Politicos', title='Resultado Final')

# horizontal bar plot
fig = px.bar(new_data,
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

# MaP
counties = {features['properties']['nombre']: random.randint(0, 300) for features in geojson['features']}
df = pd.DataFrame(list(counties.items()), columns=['Municipios', 'Votes'])

counties_pilar = {features['properties']['nombre']: random.randint(0, 300) for features in geojson_pilar['features']}
df_pilar = pd.DataFrame(list(counties_pilar.items()), columns=['Localidad', 'Votes'])

fig_map = px.choropleth_mapbox(df, geojson=geojson, color="Votes",
                            locations="Municipios", featureidkey="properties.nombre",
                            center={"lat": LOC_PILAR[0], "lon": LOC_PILAR[1]},
                            mapbox_style="carto-positron", zoom=4, opacity=0.2)

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
        html.H1(children=f"Municipio: {municipio}",
                className="header-title",),
        html.P(
            children="Analisis de las mesas electorales",
            className="header-description",
        ),
        dcc.Graph(figure=fig_results, className="card"),
        dcc.Graph(figure=fig, className="card"),
        # dcc.Graph(figure=fig_map, className="card"),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)





