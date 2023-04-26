from app.init_app import create_app
import uvicorn

app_type = input('Enter type of product: ')
app = create_app(app_type)

if __name__=='__main__':
    uvicorn.run("main:app",reload=True)