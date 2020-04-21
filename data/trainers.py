import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Trainer(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'trainers'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    img_trainer = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='https://sun9-16.userapi.com/c856028/v856028901/202200/Epy2s3_x81I.jpg')
    clientele = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='0, 0, 0')
    telefon = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='99999999999')
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

