import sqlalchemy as sa

from .db_session import SqlAlchemyBase

association_table = sa.Table('association', SqlAlchemyBase.metadata,
                             sa.Column('task_id', sa.Integer, sa.ForeignKey('task.id')),
                             sa.Column('advertiser_username', sa.Integer, sa.ForeignKey('advertiser.username')))
