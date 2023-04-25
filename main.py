from app.init_app import create_app
import uvicorn

app = create_app()

if __name__=='__main__':
    uvicorn.run("main:app",reload=True)