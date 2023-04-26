from fastapi import FastAPI
from config import getConfig,Settings
from app.databases import create_db_session,get_sql_engine, schemas 


def create_app(app_type:str):
    app = FastAPI()
    config = getConfig(app_type)
    app.config= config
    app.dbSession = init_db(config)
    register_routers(app)

    @app.get("/")
    async def root():
        return {"message": "server alive and well!!!"}
    return app

def register_routers(app:FastAPI):
    #should dynamically import modules based on app category
    from app.routers import customers,webhook
    app.include_router(customers.router,tags=['customers'])
    app.include_router(webhook.router,tags=['webhook'])
 

def init_db(config:Settings):
    db_session = create_db_session(config.sql_engine_uri)
    sql_engine = get_sql_engine(config.sql_engine_uri)
    schemas.Base.metadata.create_all(bind=sql_engine)

    return db_session
