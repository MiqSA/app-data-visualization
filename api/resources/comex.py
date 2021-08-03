from flask_restful import Resource
import pandas as pd
import json


class Comex(Resource):
    def get(self):
        data_f_comex = pd.read_csv('../datasets/f_comex.csv', sep=';')
        data_f_comex = data_f_comex[['ANO', 'MES', 'COD_NCM', 'SG_UF', 'VL_QUANTIDADE', 'MOVIMENTACAO']]
        data_f_comex = data_f_comex.to_json(orient='records')
        data_f_comex = json.loads(data_f_comex)

        return data_f_comex
    
    
class ComexLimiter(Resource):
    def get(self, id):
        data_f_comex = pd.read_csv('../datasets/f_comex.csv', sep=';', nrows=id)
        data_f_comex = data_f_comex[['ANO', 'MES', 'COD_NCM', 'SG_UF', 'VL_QUANTIDADE', 'MOVIMENTACAO']]
        data_f_comex = data_f_comex.to_json(orient='records')
        data_f_comex = json.loads(data_f_comex)
        return data_f_comex
