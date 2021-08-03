from flask_restful import Resource
import pandas as pd
import json


class Vias(Resource):
    def get(self):
        data_d_via = pd.read_excel('../datasets/d_via.xlsx')
        data_d_via = data_d_via.to_json(orient='records')
        data_d_via = json.loads(data_d_via)
        return data_d_via
