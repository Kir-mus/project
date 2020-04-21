import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    product_img = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='https://sun9-16.userapi.com/c856028/v856028901/202200/Epy2s3_x81I.jpg')
    info = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    coin = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    stories = orm.relation("Stories")


