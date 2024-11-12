from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, BigInteger
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

# Определение базы
Base = declarative_base()

# Модель таблицы "Адреса"
class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    index = Column(Integer)
    region = Column(String)
    city = Column(String)
    street = Column(String)
    number = Column(Integer)

# Модель таблицы "Тип компании"
class TypeCompany(Base):
    __tablename__ = 'type_company'
    id = Column(Integer, primary_key=True)
    name = Column(String)

# Модель таблицы "Партнеры"
class Partner(Base):
    __tablename__ = 'partners'
    id_partner = Column( Integer, primary_key=True)
    type_partner_id = Column(Integer, ForeignKey('type_company.id'))
    company_name = Column(String)
    ur_adress = Column(Integer, ForeignKey('address.id'))
    inn = Column(BigInteger)
    director_name = Column(String)
    phone = Column(String)
    email = Column(String)
    rating = Column(Integer)
    discount=Column(Integer,default=0)

    type_company = relationship("TypeCompany")
    address = relationship("Address")

# Модель таблицы "Тип продукта"
class ProductType(Base):
    __tablename__ = 'product_type'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    coefficient = Column(Float)

# Модель таблицы "Продукт"
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    type = Column(Integer, ForeignKey('product_type.id'))
    description = Column(String)
    art = Column(Integer)
    price = Column(Float)
    size = Column(Float)
    class_ = Column('class', Integer, nullable=True)

    product_type = relationship("ProductType")

# Модель таблицы "Материал"
class Material(Base):
    __tablename__ = 'material'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    defect_rate = Column(Float)

# Модель таблицы "Материал-Продукт"
class MaterialProduct(Base):
    __tablename__ = 'material_product'
    id = Column(Integer, primary_key=True)
    id_product = Column(Integer, ForeignKey('product.id'))
    id_material = Column(Integer, ForeignKey('material.id'))

    product = relationship("Product")
    material = relationship("Material")

# Модель таблицы "Партнер-Продукт"
class PartnerProduct(Base):
    __tablename__ = 'partner_product'
    id = Column(Integer, primary_key=True)
    id_product = Column(Integer, ForeignKey('product.id'))
    id_partner = Column(Integer, ForeignKey('partners.id_partner'))
    quantity = Column(Integer)
    date_of_sale = Column(Date)

    product = relationship("Product")
    partner = relationship("Partner")

# Подключение к базе данных PostgreSQL через SQLAlchemy
DATABASE_URL = "postgresql://postgres:Service@localhost:5432/z"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
