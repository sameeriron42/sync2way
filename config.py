from pydantic import BaseSettings
from dotenv import load_dotenv
import os

class Settings(BaseSettings):
    sql_engine_uri: str
    stripe_restricted_key: str
    webhook_secret: str

    class Config:
        env_file = 'app/.env'

class CustomerConfig(Settings):
    customer_tablename:str

class InvoiceConfig(Settings):
    pass

class TestConfig(Settings):
    sql_engine_uri:str
    def init(self):
        load_dotenv('app/.env')
        self.sql_engine_uri = os.getenv("TEST_SQL_ENGINE_URI")


def getConfig(config_class:str)->Settings:
    if config_class=='customer':
        return CustomerConfig()
    elif config_class=='test':
       testConf = TestConfig() 
       testConf.init()
       return testConf
    elif config_class=='invoice':
        pass