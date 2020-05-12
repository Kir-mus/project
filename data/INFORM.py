import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Info(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'inform'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='name')
    start_text = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='start_text')
    telefon = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='89999999')
    compan_img = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='https://sun9-16.userapi.com/c856028/v856028901/202200/Epy2s3_x81I.jpg')
    admin = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='admin')
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    derektor = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='derektor')


