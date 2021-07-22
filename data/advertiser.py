import sqlalchemy
from sqlalchemy import orm

from .associate import association_table
from .db_session import SqlAlchemyBase


def update_cost(username):
    # TODO подтягивание подписчиков
    return 74 * 100  # TODO определение цены


class Advertiser(SqlAlchemyBase):
    __tablename__ = 'advertiser'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True)
    cost = update_cost(username)
    tasks = orm.relationship('Task', secondary=association_table, back_populates='advertisers')
    available = sqlalchemy.Column(sqlalchemy.Boolean)
