from pydantic import BaseModel
 

class LoanDetails(BaseModel):
    amount: float
    interest: float
    downpayment: float
    term: int 

class LoanPaymentDetails(BaseModel):
    monthly_payment: float
    total_interest: float
    total_payment: float
