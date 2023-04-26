from pydantic import BaseSettings


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

def getConfig(config_class:str)->Settings:
    if config_class=='customer':
        return CustomerConfig()
    elif config_class=='invoice':
        pass