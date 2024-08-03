from pydantic import BaseModel

class Payment(BaseModel):
    loan_id: int
    pay_amount: float
