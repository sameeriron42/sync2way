from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
load_dotenv()

SQL_URL = os.getenv("SQL_ENGINE_URI")
sql_engine =create_engine(SQL_URL)

#instance of this class represents database session, 
# naming it so to distinguish from Session
SessionLocal = sessionmaker(bind=sql_engine,autoflush=False)

#Base class is inherited later to create each of the db models(tables)
Base = declarative_base()
