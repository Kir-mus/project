# import datetime
# import sqlalchemy
# from sqlalchemy import orm
# from .db_session import SqlAlchemyBase
# from sqlalchemy_serializer import SerializerMixin
#
#
# class Catalog(SqlAlchemyBase, SerializerMixin):
#     __tablename__ = 'catalog'
#     id = sqlalchemy.Column(sqlalchemy.Integer,
#                            primary_key=True, autoincrement=True)
#     name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
#     categorss = sqlalchemy.Column(sqlalchemy.String, nullable=False)
#     modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
#     categories = orm.relation("Categories")
#
