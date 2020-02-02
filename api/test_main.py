import main
import pytest

from fastapi import HTTPException
from schemas import LoanDetails, LoanPaymentDetails
from starlette.testclient import TestClient

test_client = TestClient(main.api)


def test_get_fixed_rate_loan_payment_details():
    loan_details = LoanDetails(
        amount=100000,
        interest=5.5,
        downpayment=20000,
        term=30
    )
    expected = LoanPaymentDetails(
        monthly_payment=454.23,
        total_interest=83523.23,
        total_payment=163523.23
    )
    assert main.get_fixed_rate_loan_payment_details(loan_details) == expected

def test_read_loan_payment_details():
    loan_details = LoanDetails(
        amount=123456.78,
        interest=6.36,
        downpayment=12345.67,
        term=30
    )
    expected = LoanPaymentDetails(
        monthly_payment=692.1,
        total_interest=138044.55,
        total_payment=249155.66
    )
    response = test_client.get("/payment-details", params=loan_details.dict())
    assert response.url == 'http://testserver/payment-details?amount=123456.78&interest=6.36&downpayment=12345.67&term=30'
    assert response.status_code == 200
    assert response.json() == expected.dict()

def test_read_loan_payment_details_bad_request():
    loan_details_overflow = LoanDetails(
        amount=100000,
        interest=5.5,
        downpayment=20000,
        term=3000000
    )
    response = test_client.get("/payment-details", params=loan_details_overflow.dict())
    assert response.url == 'http://testserver/payment-details?amount=100000.0&interest=5.5&downpayment=20000.0&term=3000000'
    assert response.status_code == 400
