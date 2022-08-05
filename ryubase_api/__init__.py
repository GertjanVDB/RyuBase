import json
from flask_restful import Resource,Api, reqparse
from flask import request

from logging import getLogger
logger = getLogger()


def init_api(api:Api):
    api.add_resource(DBRunRecordUpdater, '/runs/PostRunRecord')
    

class DBRunRecordUpdater(Resource):

    def post(self):
        # post to db
        import db
        
        parser= reqparse.RequestParser()
        parser.add_argument('run_id',type=str, help="Run Id")
        args=  parser.parse_args()

        json_data= request.get_json()
        logger.info(json_data)
        
        
        run_id = args['run_id']
        course_id = json_data['course_id']
        lives_at_start = json_data['lives_start']
        lives_at_end = json_data['lives_end']

        new_record = db.DBRecord(run_id,course_id,lives_at_start, lives_at_end )



        logger.info("new record: %s" % new_record)
        


        return {"message":"Ok"}, 200
