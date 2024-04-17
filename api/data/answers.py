import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, orm

from .db_session import SqlAlchemyBase


class Answer(SqlAlchemyBase):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = orm.relationship('User')
    question_id = Column(Integer, ForeignKey('questions.id'))
    question = orm.relationship('Question')
    posted = Column(DateTime, default=datetime.datetime.now)
