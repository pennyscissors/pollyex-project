import uvicorn

from fastapi import FastAPI, HTTPException
from schemas import LoanDetails, LoanPaymentDetails

api = FastAPI()


def get_fixed_rate_loan_payment_details(loan_details: LoanDetails) -> LoanPaymentDetails:
    """Get loan payment details based on input loan details.

    Calculates the monthly payment, total payment, and total 
    interest based on the a loan's amount, interest, down payment
    and term length in years.

    Args:
        loan_details (LoanDetails): Pydantic model including the 
            amount, interest, down payment and term of a loan.
    Returns:
        LoanPaymentDetail: Pydantic model obj including the monthly
        payment, total payment and total interest of a loan.

    """
    monthly_interest = (loan_details.interest / 100) / 12
    monthly_term = loan_details.term * 12
    principal = loan_details.amount - loan_details.downpayment
    a = (1 + monthly_interest) ** monthly_term

    monthly_payment = principal * ((monthly_interest * a) / (a - 1))
    total_payment = monthly_payment * monthly_term
    total_interest = total_payment - principal

    payment_details = LoanPaymentDetails(
        monthly_payment=round(monthly_payment, 2), 
        total_payment=round(total_payment, 2), 
        total_interest=round(total_interest, 2)
    )

    return payment_details

@api.get("/payment-details", response_model=LoanPaymentDetails)
def read_loan_payment_details(amount: float, interest: float, downpayment: float, term: int):
    """GET loan payment details based on given query params containing loan details.

    Args:
        amount (float): Total loan amount.
        interest (float): Interest rate for the loan.
        downpayment (float): Down payment towards principal.
        term (int): Loan term length in years.

    Returns:
        json: Returns JSON in the following format
        {
            "monthly_payment": xx.xx,
            "total_interest": xx.xx,
            "total_payment": xx.xx
        }

    """
    try:
        loan_details = LoanDetails(
            amount=amount,
            interest=interest,
            downpayment=downpayment,
            term=term
        )
        payment_details = get_fixed_rate_loan_payment_details(loan_details)
    except (ValueError, OverflowError):
        # HTTP Bad Request
        raise HTTPException(status_code=400)
    except Exception:
        # HTTP Internal Server Error
        raise HTTPException(status_code=500)

    return payment_details


if __name__ == "__main__":
    uvicorn.run(api, host = "0.0.0.0", port=80)
