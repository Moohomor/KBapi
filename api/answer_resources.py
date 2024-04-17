from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.answers import Answer

parser = reqparse.RequestParser()
parser.add_argument('content', required=True)
parser.add_argument('question_id', required=True, type=int)
parser.add_argument('author_id', required=True, type=int)


class AnswersResource(Resource):
    def get(self, answer_id):
        abort_if_answer_not_found(answer_id)
        session = db_session.create_session()
        answer = session.query(Answer).get(answer_id)
        return jsonify({'answer': dict(
            content=answer.content, author=answer.author.username,
            author_id=answer.author_id, question_id=answer.question_id, posted=answer.posted)})

    def delete(self, answer_id):
        abort_if_answer_not_found(answer_id)
        session = db_session.create_session()
        answer = session.query(Answer).get(answer_id)
        session.delete(answer)
        session.commit()
        return jsonify({'success': 'OK'})


class AnswersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        answers = session.query(Answer)
        return jsonify({'answers': [
            {'id': item.id, 'content': item.content, 'author': item.author.username,
             'author_id': item.author_id, 'question_id': item.question_id, 'posted': item.posted} for item in answers]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        answer = Answer(
            content=args['content'],
            question_id=args['question_id'],
            author_id=args['author_id']
        )
        session.add(answer)
        session.commit()
        return jsonify({'id': answer.id})


def abort_if_answer_not_found(answer_id):
    session = db_session.create_session()
    answer = session.query(Answer).get(answer_id)
    if not answer:
        abort(404, message=f"Answer No.{answer_id} not found")
