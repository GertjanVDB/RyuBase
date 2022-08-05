
import logging
from logging import getLogger, basicConfig, DEBUG, INFO
basicConfig(level=DEBUG)
logger = getLogger()

from flask import Flask
from flask_restful import Resource, Api

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
api = Api(app)

class SiteRoot(Resource):
    def get(self):
        return {"Message":"i am root"}, 200



api.add_resource(SiteRoot, '/')

logger.info('App started')

import ryubase_api



def main():
    ryubase_api.init_api(api)    
    app.run(debug=True)

if __name__ == "__main__":
    main()
    
logger.info('App Finished')