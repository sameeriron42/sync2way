from fastapi import Request 
#dependency
def get_db(request: Request):
    
    db = request.app.db_session()
    try:
        yield db
    finally:
        db.close()


