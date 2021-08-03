from flask_restful import Resource
import pandas as pd
import json


class Products(Resource):
    def get(self):
        data_d_sh2 = pd.read_excel('../datasets/d_sh2.xlsx')
        data_d_sh2 = data_d_sh2[['CO_NCM', 'NO_NCM_POR']]
        data_d_sh2['CO_NCM'] = data_d_sh2['CO_NCM'].apply(lambda x: str(x))
        data_d_sh2 = data_d_sh2.to_json(orient='records')
        data_d_sh2 = json.loads(data_d_sh2)
        return data_d_sh2
