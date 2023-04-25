from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



def create_db_session(sql_uri:str):
    sql_engine = get_sql_engine(sql_uri)
    
    #instance of this class represents database session, 
    # naming it so to distinguish from Session
    SessionLocal = sessionmaker(bind=sql_engine,autoflush=False)
    return SessionLocal

def get_sql_engine(SQL_URI:str):
    sql_engine =create_engine(SQL_URI)
    return sql_engine

#Base class is inherited later to create each of the db models(tables)
Base = declarative_base()
