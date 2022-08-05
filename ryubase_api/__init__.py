import json
from flask_restful import Resource,Api, reqparse
from flask import request

from logging import getLogger
logger = getLogger()


def init_api(api:Api):
    api.add_resource(DBUserDBUpdater, '/runs/NewUser')
    api.add_resource(DBRunDBCreator, '/runs/NewRun')
    api.add_resource(DBRunRecordUpdater, '/runs/PostRunRecord')

class DBUserDBUpdater(Resource):
    def get(self):
        # get user data for user id
        return {"message":"ok"}, 200

    def post(self):
        # create user data
        import uuid
        import db

        uid = uuid.uuid4()
        parser= reqparse.RequestParser()
        parser.add_argument('user_name',type=str, help="user display name")
        args=  parser.parse_args()
        user_name = args['user_name']
        logger.info("Creating new user")
        db.create_user(uid, user_name)
        


class DBRunDBCreator(Resource):
    def post(self):
        import db
        

        parser= reqparse.RequestParser()
        parser.add_argument('run_id',type=str, help="Run Id")
        parser.add_argument('user_id',type=str, help="user Id")
        parser.add_argument('user_name',type=str, help="user display name")

        args=  parser.parse_args()
        run_id = args['run_id']
        user_id = args['user_id']
        user_name = args['user_name']

        


        db_run = db.get_run_by_id(args['run_id'])
        if db_run:
            return {"message":"Run with id already exists"}
        else:
            
            raise NotImplemented


class DBRunRecordUpdater(Resource):

    def post(self):
        # post to db
        import db
        
        parser= reqparse.RequestParser()
        parser.add_argument('run_id',type=str, help="Run Id")
        args=  parser.parse_args()

        json_data= request.get_json()
        logger.info(json_data)
        
        db_run = db.get_run_by_id(args['run_id'])
        if not db_run:
            return {"message":"No Run exists with given run id. Create a new run first"}, 404

        run_id = args['run_id']
        course_id = json_data['course_id']
        lives_at_start = json_data['lives_start']
        lives_at_end = json_data['lives_end']

        new_record = db.DBRecord(run_id,course_id,lives_at_start, lives_at_end )

        logger.info("new record: %s" % new_record)
        
        # check if run exists
        

        return {"message":"Ok"}, 200
