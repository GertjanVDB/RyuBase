from ast import main
import logging
from logging import getLogger, basicConfig, DEBUG, INFO
basicConfig(level=DEBUG)
logger = getLogger()

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class SiteRoot(Resource):
    def get(self):
        return {"Site Root"}

api.add_resource(SiteRoot, '/')

logger.info('App started')

# imports
import db



if __name__ == "__main__":
    app.run(debug=True)
    
logger.info('App Finished')