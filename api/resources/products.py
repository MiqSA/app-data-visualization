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


class Products(Resource):
    def get(self):
        data_d_sh2 = pd.read_excel('../datasets/d_sh2.xlsx')
        data_d_sh2 = data_d_sh2[['CO_NCM', 'NO_SH2_POR']]
        data_d_sh2['CO_NCM'] = data_d_sh2['CO_NCM'] .apply(lambda x: str(x))
        msg = df_formated(data_d_sh2)
        return msg
