from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Item(Base):

    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), nullable=False)
    products_num = Column(Integer, nullable=False)
    title = Column(String(500))
    email = Column(String(500))
    phone = Column(String(20))
    inn = Column(String(12))
    psrn = Column(String(13))
    fair_business_rating = Column(String(2))
    fair_business_rating_comment = Column(String(20))
    registration_date = Column(String(20))
    main_activity = Column(String(255))
    authorized_capital = Column(String(20))
    profit = Column(String(20))
    name = Column(String(255))
    headcount = Column(String(255))


class Product(Base):

    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), nullable=False)
    product = Column(String(255), nullable=False)
