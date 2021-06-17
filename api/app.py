from flask import Flask
from flask_restful import Api
from resources.vias import Vias
from resources.products import Products


app = Flask(__name__)
api = Api(app)

api.add_resource(Vias, '/vias')
api.add_resource(Products, '/products')
api.add_resource(Products, '/comex')

if __name__ == '__main__':
    app.run(debug=True)
