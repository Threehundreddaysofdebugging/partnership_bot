import sqlalchemy
from sqlalchemy import orm

from .associate import association_table
from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase):
    __tablename__ = 'task'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    link = sqlalchemy.Column(sqlalchemy.String)
    action = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("user.id"))
    approved = sqlalchemy.Column(sqlalchemy.Boolean)
    advertisers = orm.relationship('Advertiser', secondary=association_table, back_populates='tasks')
    user = orm.relationship('User', back_populates='task')
    done = sqlalchemy.Column(sqlalchemy.Boolean)
