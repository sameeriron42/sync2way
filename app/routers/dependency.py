from fastapi import Request 
#dependency
def get_db(request: Request):
    
    db = request.app.dbSession()
    try:
        yield db
    finally:
        db.close()


