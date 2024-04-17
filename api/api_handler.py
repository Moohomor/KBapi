from flask import Flask
from flask_restful import Api
from waitress import serve

from api import question_resources, users_resources, answer_resources
from data import db_session

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/api/ping')
def ping():
    return 'pong'


if __name__ == '__main__':
    db_session.global_init('db/knowledge.sqlite')

    api.add_resource(question_resources.QuestionsListResource, '/api/q')
    api.add_resource(question_resources.QuestionsResource, '/api/q/<int:question_id>')
    api.add_resource(users_resources.UsersListResource, '/api/u')
    api.add_resource(users_resources.UsersResource, '/api/u/<int:user_id>')
    api.add_resource(answer_resources.AnswersListResource, '/api/a')
    api.add_resource(answer_resources.AnswersResource, '/api/a/<int:answer_id>')

    # app.run(port=1000)
    serve(app, port=1000)
