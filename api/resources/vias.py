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


class Vias(Resource):
    def get(self):
        data_d_via = pd.read_excel('../datasets/d_via.xlsx')
        data_d_via['CO_VIA'] = data_d_via['CO_VIA'].apply(lambda x: str(x))
        msg = df_formated(data_d_via)
        return msg
