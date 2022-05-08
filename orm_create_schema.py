from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from urllib.parse import quote_plus

Base = declarative_base()

class GroupProduct(Base):
    __tablename__ = "group_products"

    id = Column(Integer(), primary_key=True)
    name = Column(String(300), nullable=False)
    min_price = Column(Integer(), nullable=False)
    max_price = Column(Integer(), nullable=False)
    image = Column(String(300))
    products = relationship('Product', back_populates='group')
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer(), primary_key=True)
    name = Column(String(300), nullable=False)
    price = Column(Integer(), nullable=False)
    base_url = Column(String(300), nullable=False, unique=True)
    image = Column(String(300))
    group_id = Column(Integer(), ForeignKey('group_products.id'))
    group = relationship("GroupProduct", back_populates='products')
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


def persist_database(database, username, password, host, port):
    connect_string = 'mysql+pymysql://{}:{}@{}/{}'.format(username, quote_plus(password), host, database)
    if port != 3306:
        connect_string += '?port=%s' % port
    engine = create_engine(connect_string)
    Base.metadata.create_all(engine)

persist_database('test_db', 'u', 'p','h', p)
