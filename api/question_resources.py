from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.questions import Question

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('author_id', required=True, type=int)


class QuestionsResource(Resource):
    def get(self, question_id):
        abort_if_question_not_found(question_id)
        session = db_session.create_session()
        question = session.query(Question).get(question_id)
        return jsonify({'question': dict(
            title=question.title, content=question.content, author=question.author.username,
            author_id=question.author_id, answers=list(map(lambda x: x.id, question.answers)), posted=question.posted)})

    def delete(self, question_id):
        abort_if_question_not_found(question_id)
        session = db_session.create_session()
        question = session.query(Question).get(question_id)
        session.delete(question)
        session.commit()
        return jsonify({'success': 'OK'})


class QuestionsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        questions = session.query(Question)
        return jsonify({'questions': [
            {'id': item.id, 'title': item.title, 'content': item.content, 'author': item.author.username,
             'author_id': item.author_id, 'posted': item.posted} for item in questions]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        question = Question(
            title=args['title'],
            content=args['content'],
            author_id=args['author_id']
        )
        session.add(question)
        session.commit()
        return jsonify({'id': question.id})


def abort_if_question_not_found(question_id):
    session = db_session.create_session()
    question = session.query(Question).get(question_id)
    if not question:
        abort(404, message=f"Question No.{question_id} not found")
