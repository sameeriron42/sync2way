from fastapi import FastAPI
from routers import customers

app = FastAPI()

app.include_router(customers.router,tags=['customers'])

@app.get("/")
async def root():
    return{
        "message": "server alive and well!!!"
    }

