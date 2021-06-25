from flask_restful import Resource
import pandas as pd
import numpy as np


def df_formated(dataFrame):
    format_data = []
    for row in np.arange(len(dataFrame)):
        dict_data = {}
        for column in dataFrame:
            dict_data[column] = list(dataFrame[column].values)[row]
        format_data.append(dict_data)
    return format_data


class Comex(Resource):
    def get(self):
        data_f_comex = pd.read_csv('../datasets/f_comex.csv', sep=';')
        data_f_comex = data_f_comex[['ANO', 'MES', 'COD_NCM', 'SG_UF', 'VL_QUANTIDADE', 'MOVIMENTACAO']]

        data_f_comex['ANO'] = data_f_comex['ANO'].apply(lambda x: str(x))
        data_f_comex['MES'] = data_f_comex['MES'].apply(lambda x: str(x))
        data_f_comex['COD_NCM'] = data_f_comex['COD_NCM'].apply(lambda x: str(x))
        data_f_comex['SG_UF'] = data_f_comex['SG_UF'].apply(lambda x: str(x))
        data_f_comex['VL_QUANTIDADE'] = data_f_comex['VL_QUANTIDADE'].apply(lambda x: str(x))

        msg = df_formated(data_f_comex)
        return msg
    
    
class ComexLimiter(Resource):
    def get(self, id):
        data_f_comex = pd.read_csv('../datasets/f_comex.csv', sep=';', nrows=id)
        data_f_comex = data_f_comex[['ANO', 'MES', 'COD_NCM', 'SG_UF', 'VL_QUANTIDADE', 'MOVIMENTACAO']]

        data_f_comex['ANO'] = data_f_comex['ANO'].apply(lambda x: str(x))
        data_f_comex['MES'] = data_f_comex['MES'].apply(lambda x: str(x))
        data_f_comex['COD_NCM'] = data_f_comex['COD_NCM'].apply(lambda x: str(x))
        data_f_comex['SG_UF'] = data_f_comex['SG_UF'].apply(lambda x: str(x))
        data_f_comex['VL_QUANTIDADE'] = data_f_comex['VL_QUANTIDADE'].apply(lambda x: str(x))

        msg = df_formated(data_f_comex)
        return msg
