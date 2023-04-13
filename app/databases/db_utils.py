from sqlalchemy.orm import Session
from databases.models import CustomerCatalog
from routers.models import Customer

def get_users(db: Session):
    return db.query(CustomerCatalog).offset(0).limit(10).all()


def create_user(db: Session, customer: Customer):
    db_customer=CustomerCatalog(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer