from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data.users import User
from data import db_session

parser = reqparse.RequestParser()
parser.add_argument('username', required=True)


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': dict(username=user.username)})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User)
        return jsonify({'users': [{'id': item.id, 'username': item.username,
                                   'questions': item.questions} for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            username=args['username']
        )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User No.{user_id} not found")
