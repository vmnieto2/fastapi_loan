from pydantic import BaseModel

class Loan(BaseModel):
    client_id: int
    description: str
    total_loan: float
