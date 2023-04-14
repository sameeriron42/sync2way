from sqlalchemy import Column,Integer,Text
from . import Base

class CustomerCatalog(Base):
    __tablename__= "customer_catalog"

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(Text)
    email = Column(Text)

