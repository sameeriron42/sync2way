from fastapi import FastAPI
from routers import customers,webhook

app = FastAPI()

app.include_router(customers.router,tags=['customers'])
app.include_router(webhook.router,tags=['webhook'])

@app.get("/")
async def root():
    return{
        "message": "server alive and well!!!"
    }

