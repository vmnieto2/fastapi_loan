from pydantic import BaseModel

class Client(BaseModel):
    type_document: int
    document: str
    first_name: str
    second_name: str
    last_name: str
    second_last_name: str
    cell_phone: str
    email: str
