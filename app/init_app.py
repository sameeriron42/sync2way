from fastapi import FastAPI
from config import getConfig,Settings
from app.databases import create_db_session,get_sql_engine, schemas 


def create_app(app_type:str= "customer"):
    app = FastAPI()
    config = getConfig(app_type)
    app.config= config
    init_db(app,config)
    register_routers(app)

    @app.get("/")
    async def root():
        return {"message": "server alive and well!!!"}
    return app

def register_routers(current_app:FastAPI):
    #should dynamically import modules based on app category
    from app.routers import customers,webhook
    current_app.include_router(customers.router,tags=['customers'])
    current_app.include_router(webhook.router,tags=['webhook'])
 

def init_db(current_app: FastAPI,config:Settings):
    sql_engine = get_sql_engine(config.sql_engine_uri)
    current_app.db_session = create_db_session(sql_engine)
    schemas.Base.metadata.create_all(bind=sql_engine)
    current_app.sql_engine = sql_engine

