from sqlalchemy import Column, Integer, String, orm

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    questions = orm.relationship('Question', back_populates='author')
    answers = orm.relationship('Answer', back_populates='author')
