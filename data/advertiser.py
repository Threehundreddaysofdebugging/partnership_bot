import sqlalchemy
from sqlalchemy import orm

from .associate import association_table
from .db_session import SqlAlchemyBase


def get_cost(count):
    return count  # TODO определение цены


class Advertiser(SqlAlchemyBase):
    __tablename__ = 'advertiser'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True)
    # subscribers = sqlalchemy.Column(sqlalchemy.String)  # TODO подтягивание подписчиков
    # cost = get_cost(subscribers)
    tasks = orm.relationship('Task', secondary=association_table, back_populates='advertisers')
    available = sqlalchemy.Column(sqlalchemy.Boolean)
