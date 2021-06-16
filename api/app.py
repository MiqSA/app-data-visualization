from flask import Flask
from flask_restful import Api
from resources.vias import Vias


app = Flask(__name__)
api = Api(app)

api.add_resource(Vias, '/vias')

if __name__ == '__main__':
    app.run(debug=True)
