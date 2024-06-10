# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, SmallInteger, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'categories'

    categoryid = Column(Integer, primary_key=True)
    categoryname = Column(String(50))
    description = Column(String(100))


class Customer(Base):
    __tablename__ = 'customers'

    customerid = Column(String(5), primary_key=True)
    companyname = Column(String(50))
    contactname = Column(String(30))
    contacttitle = Column(String(30))
    address = Column(String(50))
    city = Column(String(20))
    region = Column(String(15))
    postalcode = Column(String(9))
    country = Column(String(15))
    phone = Column(String(17))
    fax = Column(String(17))


class Employee(Base):
    __tablename__ = 'employees'

    employeeid = Column(Integer, primary_key=True)
    lastname = Column(String(10))
    firstname = Column(String(10))
    title = Column(String(25))
    titleofcourtesy = Column(String(5))
    birthdate = Column(DateTime)
    hiredate = Column(DateTime)
    address = Column(String(50))
    city = Column(String(20))
    region = Column(String(2))
    postalcode = Column(String(9))
    country = Column(String(15))
    homephone = Column(String(14))
    extension = Column(String(4))
    reportsto = Column(Integer)
    notes = Column(Text)


class Product(Base):
    __tablename__ = 'products'

    productid = Column(Integer, primary_key=True)
    productname = Column(String(35))
    supplierid = Column(Integer, nullable=False)
    categoryid = Column(Integer, nullable=False)
    quantityperunit = Column(String(20))
    unitprice = Column(Numeric(13, 4))
    unitsinstock = Column(SmallInteger)
    unitsonorder = Column(SmallInteger)
    reorderlevel = Column(SmallInteger)
    discontinued = Column(String(1))


class Shipper(Base):
    __tablename__ = 'shippers'

    shipperid = Column(Integer, primary_key=True)
    companyname = Column(String(20))
    phone = Column(String(14))


class Supplier(Base):
    __tablename__ = 'suppliers'

    supplierid = Column(Integer, primary_key=True)
    companyname = Column(String(50))
    contactname = Column(String(30))
    contacttitle = Column(String(30))
    address = Column(String(50))
    city = Column(String(20))
    region = Column(String(15))
    postalcode = Column(String(8))
    country = Column(String(15))
    phone = Column(String(15))
    fax = Column(String(15))
    homepage = Column(String(100))


class Order(Base):
    __tablename__ = 'orders'

    orderid = Column(Integer, primary_key=True)
    customerid = Column(ForeignKey('customers.customerid', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    employeeid = Column(ForeignKey('employees.employeeid', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False)
    orderdate = Column(DateTime)
    requireddate = Column(DateTime)
    shippeddate = Column(DateTime)
    freight = Column(Numeric(15, 4))
    shipname = Column(String(35))
    shipaddress = Column(String(50))
    shipcity = Column(String(15))
    shipregion = Column(String(15))
    shippostalcode = Column(String(9))
    shipcountry = Column(String(15))
    shipperid = Column(Integer)


class OrderDetail(Base):
    __tablename__ = 'order_details'

    orderid = Column(ForeignKey('orders.orderid', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
    productid = Column(ForeignKey('products.productid', ondelete='RESTRICT', onupdate='CASCADE'), primary_key=True, nullable=False)
    unitprice = Column(Numeric(13, 4))
    quantity = Column(SmallInteger)
    discount = Column(Numeric(10, 4))

