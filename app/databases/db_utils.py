from sqlalchemy.orm import Session
from app.databases.schemas import CustomerCatalog
from app.models import Customer


def get_users(db: Session):
    return db.query(CustomerCatalog).offset(0).limit(100).all()

def get_user_by_email(db:Session,email: str):
    return db.query(CustomerCatalog).filter(CustomerCatalog.email==email).first()

def create_user(db: Session, customer: Customer):
    db_customer=CustomerCatalog(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_user(db: Session,email: str,customer: Customer):
    no_of_records = db.query(CustomerCatalog).filter(CustomerCatalog.email==email).update({"name":customer.name})
    db.commit()
    return no_of_records

def delete_user(db: Session,email:str):
    no_of_records = db.query(CustomerCatalog).filter(CustomerCatalog.email==email).delete()
    db.commit()
    return no_of_records