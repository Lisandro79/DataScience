import json
import pandas as pd
import numpy as np
from time import perf_counter

class DataSource:
    def __init__(self):
        self.invalid_codes = ['9001', '9002', '9003', '9004', '9005', '9005', '9006', '9010', '9020']
        self.elections = self.load_election_results()
        self.political_parties = self.load_political_parties()
        self.councils = self.load_councils()
        self.padron = self.load_padron()

    # Load data
    @staticmethod
    def load_padron():
        padron = pd.read_excel('./dataset/Padron_Del_Pilar-2019.xlsx')
        padron = padron.loc[3:, :]
        padron.columns = ['DNI', 'Clase', 'Apellidos', 'Nombres', 'Dirección', 'Tipo DNI', 'Circuito', 'Mesa',
                          'Sexo', 'ESCUELA', 'LOCALIDAD']
        return padron

    # Load data
    @staticmethod
    def load_election_results():
        elections = pd.read_csv('./dataset/agregados/Nuevo_elecciones_09_19.csv', low_memory=False)
        elections.columns = ['year', 'cargo', 'provincia', 'id_municipio', 'circuito', 'mesa', 'codigo_voto',
                             'cant_votos']
        return elections

    @staticmethod
    def load_political_parties():
        political_party = pd.read_csv('./dataset/agregados/Nuevo_codigo_votos_09_19.csv', low_memory=False)
        columns = ['anio', 'codigo_voto', 'nombre_partido']
        political_party.columns = columns
        return political_party

    @staticmethod
    def load_councils(dataset='./dataset/agregados/municipios_aglo.csv'):
        councils = pd.read_csv(dataset, low_memory=False)
        councils.columns = ['id_municipio', 'provincia', 'id_aglomerado', 'municipio']
        return councils

    def select_council(self, year=2019, election_type='municipales', council='PILAR'):
        id_council = self.get_council_id(council)
        df = self.elections.loc[(self.elections['cargo'] == election_type) &
                                (self.elections['id_municipio'] == id_council) &
                                (self.elections['year'] == year) &
                                (~self.elections['codigo_voto'].isin(self.invalid_codes))]
        df = df.drop(['provincia', 'id_municipio', 'circuito'], axis=1)
        return df

    def transpose_table(self, df, year):
        voting_booths = df.mesa.unique()
        parties = df['codigo_voto'].unique()
        time1 = perf_counter()
        cols_parties = [self.get_party_name(year, party) for party in parties]
        time2 = perf_counter()

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

        time3 = perf_counter()
        dataset = pd.DataFrame(res)
        dataset.columns = np.concatenate((['mesa'], cols_parties, ['total']))

        dataset.loc[:, cols_parties] = dataset.loc[:, cols_parties].div(dataset.loc[:, 'total'], axis=0)

        # print(f"Time to select political parties {time2-time1}")
        # print(f"Time to loop voting booths {time3-time2}")

        return dataset, cols_parties

    def get_council_parties(self, year, vote_ids):
        parties_names = [self.get_party_name(year, vote_id) for vote_id in vote_ids]
        return parties_names

    def get_party_name(self, year, vote_id):
        result = self.political_parties[(self.political_parties['codigo_voto'] == vote_id) &
                                        (self.political_parties['anio'] == year)]['nombre_partido'].values
        if not result:
            print("Partido not found")
            return 'None'
        else:
            return result[0]

    def get_council_id(self, council):
        result = self.councils[self.councils['municipio'] == council]['id_municipio'].values
        if not result:
            print("Municipio not found")
            return None
        else:
            return result[0]

    @staticmethod
    def get_geo_polygons(data_loc='./buenos_aires.geojson'):
        with open(data_loc) as f:
            geojson = json.load(f)
        return geojson
