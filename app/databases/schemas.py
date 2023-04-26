from sqlalchemy import Column,Integer,Text,BigInteger,Float
from . import Base

class CustomerCatalog(Base):
    __tablename__= "customer_catalog"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(Text)
    email = Column(Text)

class InvoiceCatalog(Base):
    __tablename__ = 'invoice_catalog'
    id = Column(Integer,primary_key=True,autoincrement=True)
    bill_no = Column(BigInteger,unique=True)
    amount = Column(Float)
    pass