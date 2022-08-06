import json
from flask_restful import Resource, Api, reqparse
from flask import request

from logging import getLogger

logger = getLogger()


def init_api(api: Api):
    api.add_resource(DBUserDBUpdater, '/runs/NewUser')
    api.add_resource(DBRunDBUpdater, '/runs/NewRun')
    api.add_resource(DBAttemptDBUpdater, '/runs/NewAttempt')


class DBUserDBUpdater(Resource):
    def get(self):
        # get user data for user id
        return {"message": "ok"}, 200

    def post(self):
        # create user data
        import uuid
        import db

        parser = reqparse.RequestParser()
        parser.add_argument('maker_id', type=str, help="Nintendo MakerID")
        parser.add_argument('user_name', type=str, help="user display name")
        args = parser.parse_args()
        user_name = args['user_name']
        maker_id = args['maker_id']

        logger.info("Creating new user: %s, %s" % (user_name, maker_id))
        db.create_user(maker_id, user_name)


class DBRunDBUpdater(Resource):
    def post(self):
        import db

        parser = reqparse.RequestParser()
        parser.add_argument("run_name", type=str, help="Name of this run")
        parser.add_argument("maker_id", type=str, help="Nintendo Maker id")
        args = parser.parse_args()

        run_name = args.get('run_name')
        maker_id = args.get('maker_id')

        db.create_run(run_name, maker_id)


class DBAttemptDBUpdater(Resource):
    def post(self):
        import db

        from db.data_structures import AttemptResult

        parser = reqparse.RequestParser()
        parser.add_argument('course_id', type=str, help="NintendoID of course")
        parser.add_argument('maker_id', type=str, help="Player's maker Id")
        parser.add_argument('collection_id', type=str, help="Run/Collection id")

        parser.add_argument('result_code', type=int, help="Result code of attempt, Death=0, Win=1, Skip=2")
        parser.add_argument('result_context', type=str, help="Description or cause of win/defeat/skip")
        parser.add_argument('lives_lost', type=int)
        parser.add_argument('lives_gained', type=int)

        args = parser.parse_args()

        course_id = args['course_id']
        maker_id = args['maker_id']
        collection_id = args['collection_id']

        lives_lost = args['lives_lost']
        lives_gained = args['lives_gained']
        attempt_result = args['result_code']
        attempt_result = AttemptResult(attempt_result)
        attempt_context = args['result_context']
        # checks and validation
        user_collection = db.get_collection_by_id(collection_id)
        maker = db.get_user_by_id(maker_id)

        if not lives_lost in [0, 1]:
            return {"Lives lost cannot exceed 1"}, 400
        if not lives_gained >= 0:
            return {"Lives gained must be 0 or higher"}, 400

        db.create_level_attempt(course_id,
                                maker_id,
                                collection_id,
                                attempt_result,
                                attempt_context,
                                lives_gained,
                                lives_lost
                                )
