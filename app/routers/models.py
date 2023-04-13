from pydantic import BaseModel

class Customer(BaseModel):
    id: int | None
    name: str
    email : str

    class Config:
        orm_mode = True