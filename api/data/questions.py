import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, orm

from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    author = orm.relationship('User')
    answers = orm.relationship('Answer', back_populates='question')
    posted = Column(DateTime, default=datetime.datetime.now)
