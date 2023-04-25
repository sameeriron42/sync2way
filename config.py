from pydantic import BaseSettings


class Settings(BaseSettings):
    sql_engine_uri:str
    stripe_restricted_key:str
    webhook_secret:str
    class Config:
        env_file = 'app/.env'
